"""Event-derived display state for the Hyperterminal command surface.

This module is intentionally PySide6-free so workflow display state can be
tested headlessly. The QML bridge consumes immutable snapshots from
:class:`VisualStateStore`; it never parses raw JSONL itself.
"""

from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, field

from apex_infinite.events import JsonValue

from apex_infinite_visual.events import (
    EventRecord,
    EventStateAdapter,
    LogEntry,
    WrapperSnapshot,
)

RUN_HEALTH_IDLE = "idle"
RUN_HEALTH_RUNNING = "running"
RUN_HEALTH_COMPLETE = "complete"
RUN_HEALTH_STOPPED = "stopped"
RUN_HEALTH_FAILED = "failed"

PULSE_SURFACE_CHARGE = "surface_charge"
PULSE_SIGNAL_SWEEP = "signal_sweep"
PULSE_FAULT_LOCK = "fault_lock"
PULSE_DECISION = "decision_pulse"
PULSE_PERSISTENCE_TRAIL = "persistence_trail"
PULSE_GLOW_DRAIN = "glow_drain"
PULSE_COMPLETION_SWEEP = "completion_sweep"
PULSE_ERROR_SIGNATURE = "error_signature"

PULSE_NAMES = (
    PULSE_SURFACE_CHARGE,
    PULSE_SIGNAL_SWEEP,
    PULSE_FAULT_LOCK,
    PULSE_DECISION,
    PULSE_PERSISTENCE_TRAIL,
    PULSE_GLOW_DRAIN,
    PULSE_COMPLETION_SWEEP,
    PULSE_ERROR_SIGNATURE,
)

_STAGE_BUCKETS: tuple[tuple[str, frozenset[str]], ...] = (
    (
        "startup",
        frozenset(
            {
                "startup_begin",
                "config_loaded",
                "config_resolved",
                "ui_resolved",
                "project_resolved",
                "startup",
                "autonomy_policy_resolved",
                "wrapper_capabilities_resolved",
            }
        ),
    ),
    (
        "preflight",
        frozenset(
            {
                "provider_check_started",
                "provider_check_failed",
                "provider_check_finished",
                "codex_flags_check_started",
                "codex_flags_check_failed",
                "codex_flags_check_finished",
                "codex_flags_resolved",
            }
        ),
    ),
    (
        "spec",
        frozenset(
            {
                "spec_system_detected",
                "spec_session_resolved",
                "task_progress",
                "artifact_detected",
            }
        ),
    ),
    (
        "doctor",
        frozenset({"doctor_started", "doctor_check", "doctor_finished"}),
    ),
    (
        "manager",
        frozenset(
            {
                "iteration_started",
                "history_fetched",
                "history_summary_started",
                "history_summary_completed",
                "history_summarize_started",
                "history_summarize_finished",
                "manager_decision_started",
                "manager_decision_completed",
                "manager_decision_finished",
            }
        ),
    ),
    (
        "codex",
        frozenset(
            {
                "prompt_built",
                "prompt_dispatched",
                "codex_dry_run",
                "codex_started",
                "codex_completed",
                "codex_finished",
                "output_summary",
                "response_summarized",
            }
        ),
    ),
    (
        "history",
        frozenset({"db_log_started", "db_log_finished", "db_logged"}),
    ),
    (
        "operator",
        frozenset(
            {
                "help_requested",
                "operator_interrupt_requested",
                "operator_interrupt_quit",
                "operator_input_received",
            }
        ),
    ),
    (
        "completion",
        frozenset(
            {
                "completion",
                "workflow_completed",
                "max_iterations_reached",
                "run_stopped",
            }
        ),
    ),
    (
        "fault",
        frozenset(
            {
                "codex_failed",
                "codex_timeout",
                "codex_error",
                "event_stream_error",
                "error",
            }
        ),
    ),
)


@dataclass(frozen=True)
class EventRow:  # pylint: disable=too-many-instance-attributes
    """One typed, render-ready event log row."""

    sequence: int
    severity: str
    stage: str
    title: str
    detail: str
    timestamp: str
    event: str
    iteration: int | None = None


@dataclass(frozen=True)
class SpecMapState:  # pylint: disable=too-many-instance-attributes
    """Display state for the detected Apex Spec system."""

    detected: bool = False
    has_prd: bool = False
    phase_count: int = 0
    latest_phase: str = ""
    session: str = ""
    current_command: str = ""
    tasks_done: int | None = None
    tasks_total: int | None = None


@dataclass(frozen=True)
class SignalPanelState:  # pylint: disable=too-many-instance-attributes
    """Display state for the signal/diagnostics panel."""

    provider_health: str = "unknown"
    stderr_events: int = 0
    malformed_events: int = 0
    duration_seconds: int = 0
    last_event: str = ""
    artifacts: tuple[str, ...] = ()
    capabilities_tier: str = ""


@dataclass(frozen=True)
class VisualState:  # pylint: disable=too-many-instance-attributes
    """Immutable Hyperterminal display state snapshot."""

    run_health: str = RUN_HEALTH_IDLE
    status: str = "Offline"
    stage: str = "Waiting"
    running: bool = False
    has_error: bool = False
    error_text: str = ""
    iteration: int | None = None
    project_path: str = ""
    provider_name: str = ""
    model_name: str = ""
    config_source: str = ""
    codex_flags_ok: bool | None = None
    autonomy_risk: str = ""
    autonomy_dry_run: bool | None = None
    autonomy_max_iterations: int | None = None
    manager_output: str = ""
    manager_reason: str = ""
    last_event: str = ""
    spec: SpecMapState = field(default_factory=SpecMapState)
    signal: SignalPanelState = field(default_factory=SignalPanelState)
    rows: tuple[EventRow, ...] = ()


def stage_bucket(event: str) -> str:
    """Return the display stage bucket for a registered event name."""
    for bucket, names in _STAGE_BUCKETS:
        if event in names:
            return bucket
    return "wrapper"


class VisualStateStore:  # pylint: disable=too-many-instance-attributes
    """Convert registered workflow events into Hyperterminal display state."""

    def __init__(self, max_rows: int = 400):
        self.adapter = EventStateAdapter(max_entries=max_rows)
        self._pulses: list[str] = []
        self._malformed = 0
        self._stderr_events = 0
        self._artifacts: list[str] = []
        self._config_source = ""
        self._codex_flags_ok: bool | None = None
        self._autonomy_risk = ""
        self._autonomy_dry_run: bool | None = None
        self._autonomy_max_iterations: int | None = None
        self._manager_reason = ""
        self._provider_health = "unknown"
        self._capabilities_tier = ""
        self._duration_seconds = 0
        self._start_epoch: float | None = None
        self._last_epoch: float | None = None
        self._spec = SpecMapState()
        self._iteration_rows: dict[int, int] = {}

    def ingest_line(self, line: str) -> None:
        """Consume one JSONL line, mapping malformed input to error state."""
        record = self.adapter.ingest_line(line)
        if record is None:
            self._malformed += 1
            self._pulses.append(PULSE_ERROR_SIGNATURE)
            return
        self._apply(record)

    def consume_pulses(self) -> tuple[str, ...]:
        """Drain queued event-reactive pulse triggers."""
        pulses = tuple(self._pulses)
        self._pulses.clear()
        return pulses

    def snapshot(self) -> VisualState:
        """Return an immutable display snapshot."""
        base: WrapperSnapshot = self.adapter.snapshot()
        return VisualState(
            run_health=self._run_health(base),
            status=base.status,
            stage=base.stage,
            running=base.running,
            has_error=base.has_error,
            error_text=base.error_text,
            iteration=base.iteration,
            project_path=base.project_path,
            provider_name=base.provider_name,
            model_name=base.model_name,
            config_source=self._config_source,
            codex_flags_ok=self._codex_flags_ok,
            autonomy_risk=self._autonomy_risk,
            autonomy_dry_run=self._autonomy_dry_run,
            autonomy_max_iterations=self._autonomy_max_iterations,
            manager_output=base.manager_output,
            manager_reason=self._manager_reason,
            last_event=base.last_event,
            spec=self._spec,
            signal=SignalPanelState(
                provider_health=self._provider_health,
                stderr_events=self._stderr_events,
                malformed_events=self._malformed,
                duration_seconds=self._duration_seconds,
                last_event=base.last_event,
                artifacts=tuple(self._artifacts),
                capabilities_tier=self._capabilities_tier,
            ),
            rows=tuple(self._row_from_entry(entry) for entry in base.log),
        )

    def _run_health(self, base: WrapperSnapshot) -> str:
        if base.has_error:
            return RUN_HEALTH_FAILED
        if base.running:
            return RUN_HEALTH_RUNNING
        if base.last_event in {"workflow_completed", "completion"}:
            return RUN_HEALTH_COMPLETE
        if base.last_event in {"run_stopped", "max_iterations_reached"}:
            return RUN_HEALTH_STOPPED
        return RUN_HEALTH_IDLE

    def _row_from_entry(self, entry: LogEntry) -> EventRow:
        return EventRow(
            sequence=entry.sequence,
            severity=entry.level,
            stage=stage_bucket(entry.event),
            title=entry.title,
            detail=entry.detail,
            timestamp=entry.timestamp,
            event=entry.event,
            iteration=self._iteration_rows.get(entry.sequence),
        )

    def _apply(  # pylint: disable=too-many-branches,too-many-statements
        self, record: EventRecord
    ) -> None:
        payload = record.payload
        event = record.event
        self._track_duration(record)
        if record.sequence and self.adapter.iteration is not None:
            self._iteration_rows[record.sequence] = self.adapter.iteration

        if event == "startup_begin":
            self._pulses.append(PULSE_SURFACE_CHARGE)
        elif event in {"config_loaded", "config_resolved"}:
            source = _string(payload, "config_path") or _string(payload, "source")
            if source:
                self._config_source = source
        elif event == "provider_check_finished":
            self._provider_health = "ok"
            self._pulses.append(PULSE_SIGNAL_SWEEP)
        elif event == "provider_check_failed":
            self._provider_health = "failed"
            self._pulses.append(PULSE_FAULT_LOCK)
        elif event in {"codex_flags_check_finished", "codex_flags_resolved"}:
            self._codex_flags_ok = True
        elif event == "codex_flags_check_failed":
            self._codex_flags_ok = False
            self._pulses.append(PULSE_FAULT_LOCK)
        elif event == "autonomy_policy_resolved":
            self._autonomy_risk = _string(payload, "risk_level")
            dry_run = payload.get("dry_run")
            if isinstance(dry_run, bool):
                self._autonomy_dry_run = dry_run
            self._autonomy_max_iterations = _int(payload, "max_iterations")
        elif event == "spec_system_detected":
            self._spec = SpecMapState(
                detected=bool(payload.get("detected")),
                has_prd=bool(payload.get("has_prd")),
                phase_count=_int(payload, "phase_count") or 0,
                latest_phase=_string(payload, "latest_phase"),
                session=self._spec.session,
                current_command=self._spec.current_command,
                tasks_done=self._spec.tasks_done,
                tasks_total=self._spec.tasks_total,
            )
        elif event == "spec_session_resolved":
            self._spec = _replace_spec(self._spec, session=_string(payload, "session"))
        elif event == "task_progress":
            self._spec = _replace_spec(
                self._spec,
                tasks_done=_int(payload, "done"),
                tasks_total=_int(payload, "total"),
            )
        elif event == "artifact_detected":
            name = _string(payload, "name") or _string(payload, "path")
            if name:
                self._artifacts.append(name)
        elif event == "run_duration_tick":
            seconds = _int(payload, "seconds")
            if seconds is not None:
                self._duration_seconds = seconds
        elif event == "wrapper_capabilities_resolved":
            self._capabilities_tier = _string(payload, "quality_tier")
        elif event in {"manager_decision_finished", "manager_decision_completed"}:
            self._manager_reason = _string(payload, "reason")
            self._spec = _replace_spec(
                self._spec, current_command=_string(payload, "output")
            )
            self._pulses.append(PULSE_DECISION)
        elif event == "iteration_started":
            self._pulses.append(PULSE_PERSISTENCE_TRAIL)
        elif event == "run_stopped":
            if _string(payload, "reason") == "operator_stop":
                self._pulses.append(PULSE_GLOW_DRAIN)
        elif event in {"workflow_completed", "completion"}:
            self._pulses.append(PULSE_COMPLETION_SWEEP)
        elif event in {
            "error",
            "event_stream_error",
            "codex_error",
            "codex_failed",
            "codex_timeout",
        }:
            if _string(payload, "stage") in {"stderr", "subprocess_stderr"}:
                self._stderr_events += 1
            self._pulses.append(PULSE_ERROR_SIGNATURE)

    def _track_duration(self, record: EventRecord) -> None:
        epoch = _parse_epoch(record.timestamp)
        if epoch is None:
            return
        if record.event == "startup_begin" or self._start_epoch is None:
            self._start_epoch = epoch
        self._last_epoch = epoch
        if self._start_epoch is not None and self._last_epoch >= self._start_epoch:
            self._duration_seconds = int(self._last_epoch - self._start_epoch)


def _replace_spec(spec: SpecMapState, **changes: object) -> SpecMapState:
    values: dict[str, object] = {
        "detected": spec.detected,
        "has_prd": spec.has_prd,
        "phase_count": spec.phase_count,
        "latest_phase": spec.latest_phase,
        "session": spec.session,
        "current_command": spec.current_command,
        "tasks_done": spec.tasks_done,
        "tasks_total": spec.tasks_total,
    }
    for key, value in changes.items():
        if value is not None:
            values[key] = value
    return SpecMapState(**values)  # type: ignore[arg-type]


def _string(payload: Mapping[str, JsonValue], key: str) -> str:
    value = payload.get(key)
    return value if isinstance(value, str) else ""


def _int(payload: Mapping[str, JsonValue], key: str) -> int | None:
    value = payload.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _parse_epoch(timestamp: str) -> float | None:
    try:
        return time.mktime(time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, OverflowError):
        return None
