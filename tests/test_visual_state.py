"""Visual state store tests driven by JSONL fixtures."""

import json

from apex_infinite_visual.visual_state import (
    PULSE_COMPLETION_SWEEP,
    PULSE_DECISION,
    PULSE_ERROR_SIGNATURE,
    PULSE_FAULT_LOCK,
    PULSE_GLOW_DRAIN,
    PULSE_PERSISTENCE_TRAIL,
    PULSE_SIGNAL_SWEEP,
    PULSE_SURFACE_CHARGE,
    RUN_HEALTH_COMPLETE,
    RUN_HEALTH_FAILED,
    RUN_HEALTH_RUNNING,
    RUN_HEALTH_STOPPED,
    VisualStateStore,
    stage_bucket,
)


def event_line(event, payload, timestamp="2026-07-09T00:00:00Z"):
    """Build one JSONL fixture event line."""
    return json.dumps(
        {
            "version": 1,
            "event": event,
            "timestamp": timestamp,
            "payload": payload,
        },
        ensure_ascii=True,
        sort_keys=True,
    )


def test_startup_flow_sets_identity_and_charge_pulse():
    store = VisualStateStore()
    store.ingest_line(event_line("startup_begin", {"dry_run": True}))
    store.ingest_line(
        event_line(
            "config_loaded",
            {
                "config_path": "/home/op/.config/apex-infinite/config.yaml",
                "provider_name": "ollama",
                "model_name": "qwen2.5-coder",
            },
        )
    )
    store.ingest_line(event_line("project_resolved", {"project_path": "/tmp/demo/"}))

    state = store.snapshot()
    assert state.run_health == RUN_HEALTH_RUNNING
    assert state.provider_name == "ollama"
    assert state.model_name == "qwen2.5-coder"
    assert state.config_source.endswith("config.yaml")
    assert state.project_path == "/tmp/demo/"
    assert PULSE_SURFACE_CHARGE in store.consume_pulses()


def test_provider_preflight_success_and_failure_pulses():
    store = VisualStateStore()
    store.ingest_line(event_line("provider_check_finished", {"provider_name": "o"}))
    assert store.snapshot().signal.provider_health == "ok"
    assert PULSE_SIGNAL_SWEEP in store.consume_pulses()

    store.ingest_line(
        event_line("provider_check_failed", {"provider_name": "o", "message": "down"})
    )
    assert store.snapshot().signal.provider_health == "failed"
    assert PULSE_FAULT_LOCK in store.consume_pulses()


def test_autonomy_policy_and_codex_flags_state():
    store = VisualStateStore()
    store.ingest_line(
        event_line(
            "autonomy_policy_resolved",
            {"dry_run": False, "max_iterations": 8, "risk_level": "elevated"},
        )
    )
    store.ingest_line(event_line("codex_flags_check_finished", {"flag_count": 4}))

    state = store.snapshot()
    assert state.autonomy_risk == "elevated"
    assert state.autonomy_dry_run is False
    assert state.autonomy_max_iterations == 8
    assert state.codex_flags_ok is True


def test_spec_map_accumulates_session_and_task_progress():
    store = VisualStateStore()
    store.ingest_line(
        event_line(
            "spec_system_detected",
            {
                "project_path": "/tmp/demo",
                "detected": True,
                "has_prd": True,
                "phase_count": 2,
                "latest_phase": "phase02",
            },
        )
    )
    store.ingest_line(
        event_line("spec_session_resolved", {"session": "phase02-session03"})
    )
    store.ingest_line(event_line("task_progress", {"done": 4, "total": 12}))
    store.ingest_line(
        event_line(
            "manager_decision_finished",
            {"iteration": 1, "output": "implement", "reason": "next session"},
        )
    )

    spec = store.snapshot().spec
    assert spec.detected is True
    assert spec.has_prd is True
    assert spec.latest_phase == "phase02"
    assert spec.session == "phase02-session03"
    assert spec.tasks_done == 4
    assert spec.tasks_total == 12
    assert spec.current_command == "implement"
    assert PULSE_DECISION in store.consume_pulses()


def test_iteration_completion_and_stop_pulses():
    store = VisualStateStore()
    store.ingest_line(
        event_line("iteration_started", {"iteration": 1, "operation": "implement"})
    )
    assert PULSE_PERSISTENCE_TRAIL in store.consume_pulses()

    store.ingest_line(event_line("workflow_completed", {"reason": "all done"}))
    assert store.snapshot().run_health == RUN_HEALTH_COMPLETE
    assert PULSE_COMPLETION_SWEEP in store.consume_pulses()

    store.ingest_line(
        event_line("run_stopped", {"reason": "operator_stop", "iteration": 1})
    )
    assert store.snapshot().run_health == RUN_HEALTH_STOPPED
    assert PULSE_GLOW_DRAIN in store.consume_pulses()


def test_error_events_set_failed_health_and_error_signature():
    store = VisualStateStore()
    store.ingest_line(
        event_line(
            "error",
            {"stage": "stderr", "error_type": "stderr", "message": "boom"},
        )
    )

    state = store.snapshot()
    assert state.run_health == RUN_HEALTH_FAILED
    assert state.signal.stderr_events == 1
    assert PULSE_ERROR_SIGNATURE in store.consume_pulses()


def test_malformed_lines_count_without_crashing():
    store = VisualStateStore()
    store.ingest_line("this is not json")
    store.ingest_line(event_line("startup_begin", {}))

    state = store.snapshot()
    assert state.signal.malformed_events == 1
    assert len(state.rows) == 2
    assert state.rows[0].severity == "error"


def test_duration_and_artifacts_and_capabilities():
    store = VisualStateStore()
    store.ingest_line(event_line("startup_begin", {}, timestamp="2026-07-09T00:00:00Z"))
    store.ingest_line(
        event_line(
            "artifact_detected",
            {"name": "session-spec.md"},
            timestamp="2026-07-09T00:01:30Z",
        )
    )
    store.ingest_line(
        event_line(
            "wrapper_capabilities_resolved",
            {"quality_tier": "balanced"},
            timestamp="2026-07-09T00:01:30Z",
        )
    )

    signal = store.snapshot().signal
    assert signal.duration_seconds == 90
    assert signal.artifacts == ("session-spec.md",)
    assert signal.capabilities_tier == "balanced"

    store.ingest_line(
        event_line("run_duration_tick", {"seconds": 240}, "2026-07-09T00:01:31Z")
    )
    assert store.snapshot().signal.duration_seconds >= 91


def test_rows_carry_stage_buckets_and_iterations():
    store = VisualStateStore()
    store.ingest_line(event_line("startup_begin", {}))
    store.ingest_line(
        event_line("iteration_started", {"iteration": 2, "operation": "implement"})
    )
    store.ingest_line(event_line("prompt_dispatched", {"prompt_length": 10}))

    rows = store.snapshot().rows
    assert rows[0].stage == "startup"
    assert rows[1].stage == "manager"
    assert rows[2].stage == "codex"
    assert rows[2].iteration == 2


def test_stage_bucket_classification():
    assert stage_bucket("provider_check_failed") == "preflight"
    assert stage_bucket("doctor_check") == "doctor"
    assert stage_bucket("manager_decision_finished") == "manager"
    assert stage_bucket("codex_started") == "codex"
    assert stage_bucket("db_log_finished") == "history"
    assert stage_bucket("workflow_completed") == "completion"
    assert stage_bucket("error") == "fault"
    assert stage_bucket("spec_system_detected") == "spec"
