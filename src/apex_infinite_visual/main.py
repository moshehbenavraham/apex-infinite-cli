# pylint: disable=too-many-lines
"""PySide6/Qt Quick entrypoint for the Apex Infinite Hyperterminal wrapper."""

from __future__ import annotations

import argparse
import json
import os
import queue
import sys
import threading
from dataclasses import dataclass
from pathlib import Path

from apex_infinite_visual.doctor import DoctorContext, doctor_event_rows, run_doctor
from apex_infinite_visual.launcher import (
    ApexCliLaunchError,
    ApexCliLaunchOptions,
    ApexCliProcess,
    ApexCliTimeoutError,
)
from apex_infinite_visual.profile_store import (
    ProfileStore,
    ProfileStoreError,
    load_window_state,
    save_window_state,
)
from apex_infinite_visual.render_caps import (
    RenderCapabilities,
    RenderCapsError,
    capabilities_payload,
    detect_capabilities,
    resolve_quality_tier,
)
from apex_infinite_visual.settings import (
    DEFAULT_QUALITY_TIER,
    FONT_FAMILIES,
    QUALITY_TIERS,
    RENDERING_MODES,
    THEME_CRT_GREEN,
    THEME_PLAIN,
    WRAPPER_THEME_NAMES,
    WrapperSettings,
    WrapperSettingsError,
    build_settings,
)
from apex_infinite_visual.visual_state import VisualState, VisualStateStore

SESSION_PROFILE_NAME = "last-session"


class VisualWrapperUnavailable(RuntimeError):
    """Raised when the optional graphical wrapper cannot start."""


@dataclass(frozen=True)
class VisualWrapperOptions:  # pylint: disable=too-many-instance-attributes
    """Runtime options for the Hyperterminal wrapper surface."""

    project_path: str
    start_command: str
    config_path: str | None
    provider: str | None
    model: str | None
    max_iterations: int
    dry_run: bool
    launch_cli: bool
    theme: str
    reduced_effects: bool
    auto_close_ms: int | None
    qml_path: Path
    effect_intensity: int | None = None
    font_family: str = "monospace"
    font_scale: float = 1.0
    plain_fallback: bool = False
    process_timeout_seconds: int | None = None
    rendering_mode: str | None = None
    quality_tier: str = DEFAULT_QUALITY_TIER
    font_width: float = 1.0
    line_spacing: float = 1.0
    profile: str | None = None
    restore_profile: bool = False
    profile_store_path: str | None = None


def import_qt_modules():  # pylint: disable=import-outside-toplevel
    """Import PySide6 lazily so normal package imports stay headless-safe."""
    try:
        from PySide6.QtCore import (  # pylint: disable=import-outside-toplevel
            Property,
            QObject,
            QTimer,
            QUrl,
            Signal,
            Slot,
        )
        from PySide6.QtQml import (  # pylint: disable=import-outside-toplevel
            QQmlApplicationEngine,
        )
        from PySide6.QtWidgets import (  # pylint: disable=import-outside-toplevel
            QApplication,
        )
    except ImportError as exc:
        raise VisualWrapperUnavailable(
            "PySide6 is not installed. Install the visual extra to run the "
            "optional visual wrapper."
        ) from exc
    return {
        "Property": Property,
        "QObject": QObject,
        "QTimer": QTimer,
        "QUrl": QUrl,
        "Signal": Signal,
        "Slot": Slot,
        "QQmlApplicationEngine": QQmlApplicationEngine,
        "QApplication": QApplication,
    }


def build_bridge_class(qt):  # pylint: disable=too-many-statements
    """Build the QObject bridge class after Qt modules are available."""
    property_factory = qt["Property"]
    qobject = qt["QObject"]
    signal = qt["Signal"]
    slot = qt["Slot"]
    timer = qt["QTimer"]

    class WrapperBridge(
        # pylint: disable=too-many-instance-attributes,invalid-name,too-many-public-methods
        qobject  # type: ignore[misc, valid-type]
    ):
        """Expose event-driven wrapper state and controls to QML."""

        statusChanged = signal()
        logChanged = signal()
        controlsChanged = signal()
        effectsChanged = signal()
        specChanged = signal()
        signalPanelChanged = signal()
        doctorChanged = signal()
        profilesChanged = signal()
        pulsesChanged = signal()

        def __init__(self, options: VisualWrapperOptions):
            super().__init__()
            self._options = options
            self._store = VisualStateStore(max_rows=400)
            self._state: VisualState = self._store.snapshot()
            self._log_lines: list[str] = []
            self._pulse_names: list[str] = []
            self._stage_filter = ""
            self._severity_filter = ""
            self._search_text = ""
            self._project_path = options.project_path
            self._start_command = options.start_command
            self._max_iterations = options.max_iterations
            self._dry_run = options.dry_run
            self._settings = _settings_from_options(options)
            self._profile_store: ProfileStore | None = None
            self._profile_error = ""
            self._active_profile = ""
            self._doctor_rows: list[dict[str, object]] = []
            self._doctor_status = ""
            self._doctor_ready = True
            self._caps = _detect_caps_safely()
            self._apply_capabilities()
            self._restore_profile_if_requested()
            self._apply_capabilities()
            self._theme_names = list(WRAPPER_THEME_NAMES)
            self._font_families = list(FONT_FAMILIES)
            self._rendering_modes = list(RENDERING_MODES)
            self._quality_tiers = list(QUALITY_TIERS)
            self._glow_enabled = False
            self._scanlines_enabled = False
            self._flicker_enabled = False
            self._curvature_enabled = False
            self._sync_effects_from_settings()
            self._running = False
            self._queue: queue.Queue[tuple[str, str]] = queue.Queue()
            self._worker: threading.Thread | None = None
            self._process: ApexCliProcess | None = None
            self._stop_requested = False
            self._fixture_rows: list[str] = []
            self._fixture_index = 0
            self._fixture_timer = timer(self)
            self._fixture_timer.setInterval(80)
            self._fixture_timer.timeout.connect(self._emit_next_fixture)
            self._pump_timer = timer(self)
            self._pump_timer.setInterval(50)
            self._pump_timer.timeout.connect(self._drain_queue)
            self._pump_timer.start()
            self._ingest_capabilities_event()

        @property
        def _adapter(self):
            """Backwards-compatible access to the event adapter."""
            return self._store.adapter

        # ------------------------------------------------------------------
        # Property getters
        # ------------------------------------------------------------------

        def _get_status(self) -> str:
            return self._state.status

        def _get_stage(self) -> str:
            return self._state.stage

        def _get_run_health(self) -> str:
            return self._state.run_health

        def _get_running(self) -> bool:
            return self._running or self._state.running

        def _get_has_error(self) -> bool:
            return self._state.has_error

        def _get_error_text(self) -> str:
            return self._state.error_text

        def _get_project_path(self) -> str:
            return self._project_path

        def _get_start_command(self) -> str:
            return self._start_command

        def _get_max_iterations(self) -> int:
            return self._max_iterations

        def _get_dry_run(self) -> bool:
            return self._dry_run

        def _get_provider(self) -> str:
            return self._state.provider_name or "Provider pending"

        def _get_model(self) -> str:
            return self._state.model_name or "Model pending"

        def _get_config_source(self) -> str:
            return self._state.config_source or (
                self._options.config_path or "Default config"
            )

        def _get_codex_flags_text(self) -> str:
            if self._state.codex_flags_ok is None:
                return "Not checked"
            return "Compatible" if self._state.codex_flags_ok else "Incompatible"

        def _get_event_stream_mode(self) -> str:
            return (
                "JSONL subprocess" if self._options.launch_cli else "Fixture playback"
            )

        def _get_history_db_text(self) -> str:
            history = Path.home() / ".apex-infinite" / "history.db"
            return "Present" if history.exists() else "Created on first run"

        def _get_autonomy_summary(self) -> str:
            if self._dry_run:
                return (
                    f"DRY RUN - Codex is not executed. "
                    f"Max iterations: {self._max_iterations}."
                )
            return (
                f"LIVE - Codex executes with workflow autonomy. "
                f"Max iterations: {self._max_iterations}. Risk: elevated."
            )

        def _get_iteration(self) -> str:
            if self._state.iteration is None:
                return "Not started"
            return str(self._state.iteration)

        def _get_manager_output(self) -> str:
            return self._state.manager_output or "No decision yet"

        def _get_manager_reason(self) -> str:
            return self._state.manager_reason

        def _get_log_lines(self) -> list[str]:
            return list(self._log_lines)

        def _get_event_rows(self) -> list[dict[str, object]]:
            rows = []
            for row in self._state.rows:
                if self._stage_filter and row.stage != self._stage_filter:
                    continue
                if self._severity_filter and row.severity != self._severity_filter:
                    continue
                if self._search_text:
                    haystack = f"{row.title} {row.detail} {row.event}".lower()
                    if self._search_text.lower() not in haystack:
                        continue
                rows.append(
                    {
                        "sequence": row.sequence,
                        "severity": row.severity,
                        "stage": row.stage,
                        "title": row.title,
                        "detail": row.detail,
                        "timestamp": row.timestamp,
                        "event": row.event,
                        "iteration": -1 if row.iteration is None else row.iteration,
                    }
                )
            return rows

        def _get_stage_filter(self) -> str:
            return self._stage_filter

        def _get_severity_filter(self) -> str:
            return self._severity_filter

        def _get_search_text(self) -> str:
            return self._search_text

        def _get_pulse_names(self) -> list[str]:
            return list(self._pulse_names)

        # Spec map -----------------------------------------------------------

        def _get_spec_detected(self) -> bool:
            return self._state.spec.detected

        def _get_spec_phase(self) -> str:
            spec = self._state.spec
            if not spec.detected:
                return "No spec system"
            if spec.latest_phase:
                return f"{spec.latest_phase} of {spec.phase_count}"
            return f"{spec.phase_count} phase(s)"

        def _get_spec_session(self) -> str:
            return self._state.spec.session or "Session pending"

        def _get_spec_command(self) -> str:
            return self._state.spec.current_command or "No command yet"

        def _get_task_progress_text(self) -> str:
            spec = self._state.spec
            if spec.tasks_done is None or spec.tasks_total is None:
                return "No task data"
            return f"{spec.tasks_done} / {spec.tasks_total}"

        def _get_task_progress_ratio(self) -> float:
            spec = self._state.spec
            if not spec.tasks_total:
                return 0.0
            done = spec.tasks_done or 0
            return max(0.0, min(1.0, done / spec.tasks_total))

        # Signal panel --------------------------------------------------------

        def _get_provider_health(self) -> str:
            return self._state.signal.provider_health

        def _get_stderr_events(self) -> int:
            return self._state.signal.stderr_events

        def _get_malformed_events(self) -> int:
            return self._state.signal.malformed_events

        def _get_duration_text(self) -> str:
            seconds = self._state.signal.duration_seconds
            minutes, secs = divmod(max(0, seconds), 60)
            return f"{minutes:02d}:{secs:02d}"

        def _get_last_event(self) -> str:
            return self._state.last_event or "None"

        def _get_artifacts(self) -> list[str]:
            return list(self._state.signal.artifacts)

        # Capabilities ---------------------------------------------------------

        def _get_backend_name(self) -> str:
            return self._caps.backend if self._caps else "unknown"

        def _get_shaders_available(self) -> bool:
            return bool(self._caps and self._caps.shaders_available)

        def _get_recommended_tier(self) -> str:
            return self._caps.recommended_tier if self._caps else DEFAULT_QUALITY_TIER

        # Doctor ---------------------------------------------------------------

        def _get_doctor_rows(self) -> list[dict[str, object]]:
            return list(self._doctor_rows)

        def _get_doctor_status(self) -> str:
            return self._doctor_status

        def _get_doctor_ready(self) -> bool:
            return self._doctor_ready

        def _get_first_run_needed(self) -> bool:
            if self._options.config_path:
                return not Path(os.path.expanduser(self._options.config_path)).is_file()
            return not (Path.cwd() / "config.yaml").is_file()

        # Profiles -------------------------------------------------------------

        def _get_profile_names(self) -> list[str]:
            store = self._ensure_profile_store()
            if store is None:
                return []
            return store.profile_names()

        def _get_active_profile(self) -> str:
            return self._active_profile

        def _get_profile_error(self) -> str:
            return self._profile_error

        # Visual settings --------------------------------------------------------

        def _get_theme(self) -> str:
            return self._settings.theme_name

        def _get_effective_theme(self) -> str:
            return self._settings.effective_theme_name

        def _get_theme_names(self) -> list[str]:
            return list(self._theme_names)

        def _get_theme_label(self) -> str:
            return self._settings.preset.label

        def _get_rendering_mode(self) -> str:
            return self._settings.rendering_mode

        def _get_effective_rendering_mode(self) -> str:
            return self._settings.effective_rendering_mode

        def _get_rendering_modes(self) -> list[str]:
            return list(self._rendering_modes)

        def _get_quality_tier(self) -> str:
            return self._settings.quality_tier

        def _get_effective_quality_tier(self) -> str:
            return self._settings.effective_quality_tier

        def _get_quality_tiers(self) -> list[str]:
            return list(self._quality_tiers)

        def _get_effect_fps(self) -> int:
            return self._settings.effect_fps

        def _get_reduced_effects(self) -> bool:
            return self._settings.reduced_effects

        def _get_plain_fallback(self) -> bool:
            return (
                self._settings.plain_fallback
                or self._settings.theme_name == THEME_PLAIN
            )

        def _get_effect_intensity(self) -> int:
            return self._settings.effect_intensity

        def _get_effect_opacity(self) -> float:
            return self._settings.effect_opacity

        def _get_font_family(self) -> str:
            return self._settings.font_family

        def _get_font_scale(self) -> float:
            return self._settings.font_scale

        def _get_font_width(self) -> float:
            return self._settings.font_width

        def _get_line_spacing(self) -> float:
            return self._settings.line_spacing

        def _get_font_families(self) -> list[str]:
            return list(self._font_families)

        def _color(self, key: str) -> str:
            return self._settings.color_map()[key]

        def _get_background_color(self) -> str:
            return self._color("background")

        def _get_panel_color(self) -> str:
            return self._color("panel")

        def _get_panel_alt_color(self) -> str:
            return self._color("panel_alt")

        def _get_cell_color(self) -> str:
            return self._color("cell")

        def _get_border_color(self) -> str:
            return self._color("border")

        def _get_accent_color(self) -> str:
            return self._color("accent")

        def _get_text_color(self) -> str:
            return self._color("text")

        def _get_muted_color(self) -> str:
            return self._color("muted")

        def _get_warning_color(self) -> str:
            return self._color("warning")

        def _get_error_color(self) -> str:
            return self._color("error")

        def _get_glow_enabled(self) -> bool:
            return self._glow_enabled

        def _get_scanlines_enabled(self) -> bool:
            return self._scanlines_enabled

        def _get_flicker_enabled(self) -> bool:
            return self._flicker_enabled

        def _get_curvature_enabled(self) -> bool:
            return self._curvature_enabled

        def _get_bloom_enabled(self) -> bool:
            return self._settings.effect_enabled("bloom")

        def _get_persistence_enabled(self) -> bool:
            return self._settings.effect_enabled("persistence")

        def _get_noise_enabled(self) -> bool:
            return self._settings.effect_enabled("noise")

        def _get_jitter_enabled(self) -> bool:
            return self._settings.effect_enabled("jitter")

        def _get_sync_enabled(self) -> bool:
            return self._settings.effect_enabled("sync")

        def _get_chroma_enabled(self) -> bool:
            return self._settings.effect_enabled("chroma")

        def _get_ambient_frame_enabled(self) -> bool:
            return self._settings.effect_enabled("ambient_frame")

        # ------------------------------------------------------------------
        # Qt properties
        # ------------------------------------------------------------------

        statusText = property_factory(str, _get_status, notify=statusChanged)
        stageText = property_factory(str, _get_stage, notify=statusChanged)
        runHealth = property_factory(str, _get_run_health, notify=statusChanged)
        running = property_factory(bool, _get_running, notify=statusChanged)
        hasError = property_factory(bool, _get_has_error, notify=statusChanged)
        errorText = property_factory(str, _get_error_text, notify=statusChanged)
        projectPath = property_factory(str, _get_project_path, notify=controlsChanged)
        startCommand = property_factory(str, _get_start_command, notify=controlsChanged)
        maxIterations = property_factory(
            int, _get_max_iterations, notify=controlsChanged
        )
        dryRun = property_factory(bool, _get_dry_run, notify=controlsChanged)
        autonomySummary = property_factory(
            str, _get_autonomy_summary, notify=controlsChanged
        )
        providerName = property_factory(str, _get_provider, notify=statusChanged)
        modelName = property_factory(str, _get_model, notify=statusChanged)
        configSource = property_factory(str, _get_config_source, notify=statusChanged)
        codexFlagsText = property_factory(
            str, _get_codex_flags_text, notify=statusChanged
        )
        eventStreamMode = property_factory(
            str, _get_event_stream_mode, notify=controlsChanged
        )
        historyDbText = property_factory(
            str, _get_history_db_text, notify=statusChanged
        )
        iterationText = property_factory(str, _get_iteration, notify=statusChanged)
        managerOutput = property_factory(str, _get_manager_output, notify=statusChanged)
        managerReason = property_factory(str, _get_manager_reason, notify=statusChanged)
        logLines = property_factory("QStringList", _get_log_lines, notify=logChanged)
        eventRows = property_factory("QVariantList", _get_event_rows, notify=logChanged)
        stageFilter = property_factory(str, _get_stage_filter, notify=logChanged)
        severityFilter = property_factory(str, _get_severity_filter, notify=logChanged)
        searchText = property_factory(str, _get_search_text, notify=logChanged)
        pulseNames = property_factory(
            "QStringList", _get_pulse_names, notify=pulsesChanged
        )
        specDetected = property_factory(bool, _get_spec_detected, notify=specChanged)
        specPhase = property_factory(str, _get_spec_phase, notify=specChanged)
        specSession = property_factory(str, _get_spec_session, notify=specChanged)
        specCommand = property_factory(str, _get_spec_command, notify=specChanged)
        taskProgressText = property_factory(
            str, _get_task_progress_text, notify=specChanged
        )
        taskProgressRatio = property_factory(
            float, _get_task_progress_ratio, notify=specChanged
        )
        providerHealth = property_factory(
            str, _get_provider_health, notify=signalPanelChanged
        )
        stderrEvents = property_factory(
            int, _get_stderr_events, notify=signalPanelChanged
        )
        malformedEvents = property_factory(
            int, _get_malformed_events, notify=signalPanelChanged
        )
        durationText = property_factory(
            str, _get_duration_text, notify=signalPanelChanged
        )
        lastEvent = property_factory(str, _get_last_event, notify=signalPanelChanged)
        artifacts = property_factory(
            "QStringList", _get_artifacts, notify=signalPanelChanged
        )
        backendName = property_factory(str, _get_backend_name, notify=effectsChanged)
        shadersAvailable = property_factory(
            bool, _get_shaders_available, notify=effectsChanged
        )
        recommendedTier = property_factory(
            str, _get_recommended_tier, notify=effectsChanged
        )
        doctorRows = property_factory(
            "QVariantList", _get_doctor_rows, notify=doctorChanged
        )
        doctorStatus = property_factory(str, _get_doctor_status, notify=doctorChanged)
        doctorLaunchReady = property_factory(
            bool, _get_doctor_ready, notify=doctorChanged
        )
        firstRunNeeded = property_factory(
            bool, _get_first_run_needed, notify=doctorChanged
        )
        profileNames = property_factory(
            "QStringList", _get_profile_names, notify=profilesChanged
        )
        activeProfile = property_factory(
            str, _get_active_profile, notify=profilesChanged
        )
        profileError = property_factory(str, _get_profile_error, notify=profilesChanged)
        themeName = property_factory(str, _get_theme, notify=effectsChanged)
        effectiveThemeName = property_factory(
            str, _get_effective_theme, notify=effectsChanged
        )
        themeNames = property_factory(
            "QStringList", _get_theme_names, notify=effectsChanged
        )
        themeLabel = property_factory(str, _get_theme_label, notify=effectsChanged)
        renderingMode = property_factory(
            str, _get_rendering_mode, notify=effectsChanged
        )
        effectiveRenderingMode = property_factory(
            str, _get_effective_rendering_mode, notify=effectsChanged
        )
        renderingModes = property_factory(
            "QStringList", _get_rendering_modes, notify=effectsChanged
        )
        qualityTier = property_factory(str, _get_quality_tier, notify=effectsChanged)
        effectiveQualityTier = property_factory(
            str, _get_effective_quality_tier, notify=effectsChanged
        )
        qualityTiers = property_factory(
            "QStringList", _get_quality_tiers, notify=effectsChanged
        )
        effectFps = property_factory(int, _get_effect_fps, notify=effectsChanged)
        reducedEffects = property_factory(
            bool, _get_reduced_effects, notify=effectsChanged
        )
        plainFallback = property_factory(
            bool, _get_plain_fallback, notify=effectsChanged
        )
        effectIntensity = property_factory(
            int, _get_effect_intensity, notify=effectsChanged
        )
        effectOpacity = property_factory(
            float, _get_effect_opacity, notify=effectsChanged
        )
        fontFamily = property_factory(str, _get_font_family, notify=effectsChanged)
        fontScale = property_factory(float, _get_font_scale, notify=effectsChanged)
        fontWidth = property_factory(float, _get_font_width, notify=effectsChanged)
        lineSpacing = property_factory(float, _get_line_spacing, notify=effectsChanged)
        fontFamilies = property_factory(
            "QStringList", _get_font_families, notify=effectsChanged
        )
        backgroundColor = property_factory(
            str, _get_background_color, notify=effectsChanged
        )
        panelColor = property_factory(str, _get_panel_color, notify=effectsChanged)
        panelAltColor = property_factory(
            str, _get_panel_alt_color, notify=effectsChanged
        )
        cellColor = property_factory(str, _get_cell_color, notify=effectsChanged)
        borderColor = property_factory(str, _get_border_color, notify=effectsChanged)
        accentColor = property_factory(str, _get_accent_color, notify=effectsChanged)
        textColor = property_factory(str, _get_text_color, notify=effectsChanged)
        mutedColor = property_factory(str, _get_muted_color, notify=effectsChanged)
        warningColor = property_factory(str, _get_warning_color, notify=effectsChanged)
        errorColor = property_factory(str, _get_error_color, notify=effectsChanged)
        glowEnabled = property_factory(bool, _get_glow_enabled, notify=effectsChanged)
        scanlinesEnabled = property_factory(
            bool, _get_scanlines_enabled, notify=effectsChanged
        )
        flickerEnabled = property_factory(
            bool, _get_flicker_enabled, notify=effectsChanged
        )
        curvatureEnabled = property_factory(
            bool, _get_curvature_enabled, notify=effectsChanged
        )
        bloomEnabled = property_factory(bool, _get_bloom_enabled, notify=effectsChanged)
        persistenceEnabled = property_factory(
            bool, _get_persistence_enabled, notify=effectsChanged
        )
        noiseEnabled = property_factory(bool, _get_noise_enabled, notify=effectsChanged)
        jitterEnabled = property_factory(
            bool, _get_jitter_enabled, notify=effectsChanged
        )
        syncEnabled = property_factory(bool, _get_sync_enabled, notify=effectsChanged)
        chromaEnabled = property_factory(
            bool, _get_chroma_enabled, notify=effectsChanged
        )
        ambientFrameEnabled = property_factory(
            bool, _get_ambient_frame_enabled, notify=effectsChanged
        )

        # ------------------------------------------------------------------
        # Run control slots
        # ------------------------------------------------------------------

        @slot()
        def startRun(self) -> None:
            """Start fixture playback or the real guarded CLI subprocess."""
            if self._running:
                return
            self._running = True
            self._stop_requested = False
            self.statusChanged.emit()
            if self._options.launch_cli:
                self._start_process_worker()
                return
            self._start_fixture_flow()

        @slot()
        def stopRun(self) -> None:
            """Stop the current fixture or subprocess lifecycle."""
            if not self._running and not self._state.running:
                return
            self._stop_requested = True
            if self._fixture_timer.isActive():
                self._fixture_timer.stop()
            if self._process:
                self._process.terminate()
            self._running = False
            self._ingest_synthetic_event(
                "run_stopped", {"reason": "operator_stop", "iteration": 0}
            )
            self.statusChanged.emit()

        @slot()
        def shutdown(self) -> None:
            """Release timers and subprocess resources before wrapper exit."""
            if self._fixture_timer.isActive():
                self._fixture_timer.stop()
            if self._pump_timer.isActive():
                self._pump_timer.stop()
            if self._process:
                self._process.terminate()
            self._running = False
            self._persist_session_profile()

        @slot()
        def runDoctor(self) -> None:
            """Run launch-readiness diagnostics and publish results."""
            context = DoctorContext(
                project_path=self._project_path,
                config_path=self._options.config_path or "",
            )
            self._ingest_synthetic_event("doctor_started", {"source": "wrapper"})
            report = run_doctor(context)
            rows = doctor_event_rows(report)
            for row in rows:
                self._ingest_synthetic_event("doctor_check", row)
            self._ingest_synthetic_event(
                "doctor_finished",
                {
                    "status": report.status,
                    "launch_ready": report.launch_ready,
                    **report.counts(),
                },
            )
            self._doctor_rows = rows
            self._doctor_status = report.status
            self._doctor_ready = report.launch_ready
            self.doctorChanged.emit()

        @slot(int, int)
        def storeWindowGeometry(self, width: int, height: int) -> None:
            """Persist runtime window geometry under XDG state."""
            if not self._options.restore_profile:
                return
            try:
                save_window_state({"width": int(width), "height": int(height)})
            except ProfileStoreError:
                pass

        @slot(str)
        def setProjectPath(self, value: str) -> None:
            """Update the project path control."""
            if self._running:
                return
            self._project_path = value.strip() or os.getcwd()
            self.controlsChanged.emit()

        @slot(str)
        def setStartCommand(self, value: str) -> None:
            """Update the optional start command control."""
            if self._running:
                return
            self._start_command = value.strip()
            self.controlsChanged.emit()

        @slot(int)
        def setMaxIterations(self, value: int) -> None:
            """Update the max-iteration control."""
            if self._running:
                return
            self._max_iterations = max(1, int(value))
            self.controlsChanged.emit()

        @slot(bool)
        def setDryRun(self, value: bool) -> None:
            """Update dry-run mode."""
            if self._running:
                return
            self._dry_run = bool(value)
            self.controlsChanged.emit()

        # ------------------------------------------------------------------
        # Event log filter slots
        # ------------------------------------------------------------------

        @slot(str)
        def exportEvents(self, path: str) -> None:
            """Export the current filtered event rows as JSON."""
            target = Path(os.path.expanduser(path))
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    json.dumps(
                        self._get_event_rows(),
                        ensure_ascii=True,
                        sort_keys=True,
                        indent=2,
                    )
                    + "\n",
                    encoding="ascii",
                )
            except OSError as exc:
                self._ingest_synthetic_event(
                    "error",
                    {
                        "stage": "wrapper",
                        "error_type": "export_failed",
                        "message": f"Event export failed: {exc.__class__.__name__}",
                    },
                )

        @slot(str)
        def setStageFilter(self, value: str) -> None:
            """Filter event rows by stage bucket ('' clears)."""
            self._stage_filter = value.strip()
            self.logChanged.emit()

        @slot(str)
        def setSeverityFilter(self, value: str) -> None:
            """Filter event rows by severity ('' clears)."""
            self._severity_filter = value.strip()
            self.logChanged.emit()

        @slot(str)
        def setSearchText(self, value: str) -> None:
            """Filter event rows by free text ('' clears)."""
            self._search_text = value.strip()
            self.logChanged.emit()

        # ------------------------------------------------------------------
        # Visual settings slots
        # ------------------------------------------------------------------

        @slot(str)
        def setTheme(self, value: str) -> None:
            """Update the QML theme selector."""
            plain_fallback = value == THEME_PLAIN
            self._update_settings(theme_name=value, plain_fallback=plain_fallback)

        @slot(str)
        def setRenderingMode(self, value: str) -> None:
            """Update the operator rendering mode."""
            self._update_settings(rendering_mode=value)

        @slot(str)
        def setQualityTier(self, value: str) -> None:
            """Update the effect quality tier, clamped to capabilities."""
            resolved = value
            if self._caps is not None:
                try:
                    resolved = resolve_quality_tier(value, self._caps)
                except RenderCapsError as exc:
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "settings",
                            "error_type": "invalid_settings",
                            "message": str(exc),
                        },
                    )
                    return
            self._update_settings(quality_tier=resolved)

        @slot(bool)
        def setReducedEffects(self, value: bool) -> None:
            """Apply the reduced-effects fallback."""
            self._update_settings(reduced_effects=bool(value))

        @slot(int)
        def setEffectIntensity(self, value: int) -> None:
            """Update the bounded effect intensity."""
            self._update_settings(effect_intensity=max(0, min(100, int(value))))

        @slot(str)
        def setFontFamily(self, value: str) -> None:
            """Update the wrapper font family."""
            self._update_settings(font_family=value.strip() or "monospace")

        @slot(float)
        def setFontScale(self, value: float) -> None:
            """Update the wrapper font scale."""
            self._update_settings(font_scale=round(float(value), 2))

        @slot(float)
        def setFontWidth(self, value: float) -> None:
            """Update the wrapper font width factor."""
            self._update_settings(font_width=round(float(value), 2))

        @slot(float)
        def setLineSpacing(self, value: float) -> None:
            """Update the event row line spacing factor."""
            self._update_settings(line_spacing=round(float(value), 2))

        @slot(bool)
        def setPlainFallback(self, value: bool) -> None:
            """Apply or clear the plain fallback surface."""
            if self._settings.theme_name == THEME_PLAIN and not value:
                self._update_settings(theme_name=THEME_CRT_GREEN, plain_fallback=False)
                return
            self._update_settings(plain_fallback=bool(value))

        @slot(str, bool)
        def setEffectEnabled(self, name: str, value: bool) -> None:
            """Update one independent visual effect control."""
            enabled = bool(value) and self._settings.effects_available
            if name == "glow":
                self._glow_enabled = enabled
            elif name == "scanlines":
                self._scanlines_enabled = enabled
            elif name == "flicker":
                self._flicker_enabled = enabled
            elif name == "curvature":
                self._curvature_enabled = enabled
            self.effectsChanged.emit()

        # ------------------------------------------------------------------
        # Profile slots
        # ------------------------------------------------------------------

        @slot(str)
        def saveProfile(self, name: str) -> None:
            """Save current visual settings as a named custom profile."""
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                store.save_current(name, self._settings, effects=self._current_effects())
                self._active_profile = name
                self._profile_error = ""
            except ProfileStoreError as exc:
                self._profile_error = str(exc)
            self.profilesChanged.emit()

        @slot(str)
        def loadProfile(self, name: str) -> None:
            """Load a built-in or custom profile."""
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                profile = store.get(name)
                self._settings = profile.to_settings()
                self._apply_capabilities()
                self._active_profile = name
                self._profile_error = ""
                store.set_last_profile(name)
            except (ProfileStoreError, WrapperSettingsError) as exc:
                self._profile_error = str(exc)
                self.profilesChanged.emit()
                return
            self._sync_effects_from_settings()
            self.effectsChanged.emit()
            self.profilesChanged.emit()

        @slot(str)
        def deleteProfile(self, name: str) -> None:
            """Delete a custom profile."""
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                store.delete(name)
                if self._active_profile == name:
                    self._active_profile = ""
                self._profile_error = ""
            except ProfileStoreError as exc:
                self._profile_error = str(exc)
            self.profilesChanged.emit()

        @slot(str, str)
        def duplicateProfile(self, source: str, target: str) -> None:
            """Duplicate a profile to a new custom name."""
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                store.duplicate(source, target)
                self._profile_error = ""
            except ProfileStoreError as exc:
                self._profile_error = str(exc)
            self.profilesChanged.emit()

        @slot(str, str)
        def exportProfile(self, name: str, path: str) -> None:
            """Export one profile as JSON."""
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                store.export_profile(name, Path(os.path.expanduser(path)))
                self._profile_error = ""
            except (ProfileStoreError, OSError) as exc:
                self._profile_error = str(exc)
            self.profilesChanged.emit()

        @slot(str)
        def importProfile(self, path: str) -> None:
            """Import one profile JSON file."""
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                store.import_profile(Path(os.path.expanduser(path)))
                self._profile_error = ""
            except ProfileStoreError as exc:
                self._profile_error = str(exc)
            self.profilesChanged.emit()

        # ------------------------------------------------------------------
        # Internal helpers
        # ------------------------------------------------------------------

        def _ensure_profile_store(self) -> ProfileStore | None:
            if self._profile_store is not None:
                return self._profile_store
            try:
                if self._options.profile_store_path:
                    self._profile_store = ProfileStore(
                        Path(self._options.profile_store_path)
                    )
                else:
                    self._profile_store = ProfileStore()
            except ProfileStoreError as exc:
                self._profile_error = str(exc)
                return None
            if self._profile_store.load_error:
                self._profile_error = self._profile_store.load_error
            return self._profile_store

        def _restore_profile_if_requested(self) -> None:
            wanted = self._options.profile
            if not wanted and not self._options.restore_profile:
                return
            store = self._ensure_profile_store()
            if store is None:
                return
            name = wanted or store.last_profile
            if not name:
                return
            try:
                self._settings = store.get(name).to_settings()
                self._apply_capabilities()
                self._active_profile = name
            except (ProfileStoreError, WrapperSettingsError) as exc:
                self._profile_error = str(exc)

        def _detect_caps(self) -> RenderCapabilities | None:
            return self._caps

        def _apply_capabilities(self) -> None:
            if self._caps is None:
                return
            try:
                resolved = resolve_quality_tier(self._settings.quality_tier, self._caps)
                changes: dict[str, object] = {}
                if resolved != self._settings.quality_tier:
                    changes["quality_tier"] = resolved
                if self._caps.reduced_effects_forced:
                    changes["reduced_effects"] = True
                if changes:
                    self._settings = self._settings.updated(**changes)
            except (RenderCapsError, WrapperSettingsError):
                pass

        def _ingest_capabilities_event(self) -> None:
            if self._caps is None:
                return
            self._ingest_synthetic_event(
                "wrapper_capabilities_resolved", capabilities_payload(self._caps)
            )

        def _start_fixture_flow(self) -> None:
            self._reset_store()
            self._fixture_rows = build_fixture_event_lines(
                self._project_path,
                self._start_command or "implement",
                self._max_iterations,
            )
            self._fixture_index = 0
            self._fixture_timer.start()

        def _emit_next_fixture(self) -> None:
            if self._fixture_index >= len(self._fixture_rows):
                self._fixture_timer.stop()
                self._running = False
                self.statusChanged.emit()
                return
            self._store.ingest_line(self._fixture_rows[self._fixture_index])
            self._fixture_index += 1
            self._refresh_snapshot()

        def _start_process_worker(self) -> None:
            self._reset_store()
            self._worker = threading.Thread(target=self._run_process, daemon=True)
            self._worker.start()

        def _run_process(self) -> None:
            launch_options = ApexCliLaunchOptions(
                project_path=self._project_path,
                start_command=self._start_command or None,
                config_path=self._options.config_path,
                provider=self._options.provider,
                model=self._options.model,
                max_iterations=self._max_iterations,
                dry_run=self._dry_run,
                process_timeout_seconds=self._options.process_timeout_seconds,
            )
            try:
                with ApexCliProcess(launch_options) as process:
                    self._process = process
                    stderr_chunks: list[str] = []
                    stdout_reader = threading.Thread(
                        target=self._read_stdout,
                        args=(process,),
                        daemon=True,
                    )
                    stderr_reader = threading.Thread(
                        target=self._read_stderr,
                        args=(process, stderr_chunks),
                        daemon=True,
                    )
                    stdout_reader.start()
                    stderr_reader.start()
                    try:
                        if hasattr(process, "wait"):
                            return_code = process.wait()
                        elif process.process:
                            return_code = process.process.wait()
                        else:
                            return_code = 0
                    finally:
                        stdout_reader.join()
                        stderr_reader.join()
                    stderr = "".join(stderr_chunks)
                    if self._stop_requested:
                        return
                    if stderr.strip():
                        self._queue.put(("stderr", stderr.strip()))
                    if return_code:
                        self._queue.put(("return_code", str(int(return_code))))
            except ApexCliTimeoutError as exc:
                self._queue.put(("timeout", str(exc.timeout_seconds)))
            except ApexCliLaunchError as exc:
                self._queue.put(
                    (
                        "launch_error",
                        json.dumps(
                            {
                                "error_type": exc.code,
                                "message": exc.message,
                            },
                            ensure_ascii=True,
                            sort_keys=True,
                        ),
                    )
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self._queue.put(("error", exc.__class__.__name__))
            finally:
                self._process = None
                self._queue.put(("done", ""))

        def _read_stdout(self, process: ApexCliProcess) -> None:
            for line in process.iter_stdout_lines():
                self._queue.put(("line", line))

        def _read_stderr(
            self, process: ApexCliProcess, stderr_chunks: list[str]
        ) -> None:
            stderr_chunks.append(process.read_stderr())

        def _drain_queue(self) -> None:
            changed = False
            while True:
                try:
                    kind, value = self._queue.get_nowait()
                except queue.Empty:
                    break
                changed = True
                if kind == "line":
                    self._store.ingest_line(value)
                elif kind == "stderr":
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "stderr",
                            "error_type": "stderr",
                            "message": _stderr_summary(value),
                        },
                    )
                elif kind == "return_code":
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "subprocess",
                            "error_type": "non_zero_exit",
                            "return_code": int(value),
                        },
                    )
                elif kind == "timeout":
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "subprocess",
                            "error_type": "timeout",
                            "timeout_seconds": int(value),
                        },
                    )
                elif kind == "launch_error":
                    payload = json.loads(value)
                    self._ingest_synthetic_event(
                        "error",
                        {"stage": "launch_validation", **payload},
                    )
                elif kind == "error":
                    self._ingest_synthetic_event(
                        "error",
                        {"stage": "wrapper", "error_type": value},
                    )
                elif kind == "done":
                    self._running = False
            if changed:
                self._refresh_snapshot()

        def _ingest_synthetic_event(
            self, event: str, payload: dict[str, object]
        ) -> None:
            row = {
                "version": 1,
                "event": event,
                "timestamp": "2026-07-03T00:00:00Z",
                "payload": payload,
            }
            self._store.ingest_line(json.dumps(row, ensure_ascii=True))
            self._refresh_snapshot()

        def _reset_store(self) -> None:
            self._store = VisualStateStore(max_rows=400)
            self._state = self._store.snapshot()
            self._log_lines = []
            self.statusChanged.emit()
            self.logChanged.emit()
            self.specChanged.emit()
            self.signalPanelChanged.emit()

        # Backwards-compatible alias used by earlier tests and tooling.
        _reset_adapter = _reset_store

        def _refresh_snapshot(self) -> None:
            self._state = self._store.snapshot()
            self._log_lines = [_format_log_line(entry) for entry in self._state.rows]
            pulses = self._store.consume_pulses()
            if pulses:
                self._pulse_names = list(pulses)
                self.pulsesChanged.emit()
            self.statusChanged.emit()
            self.logChanged.emit()
            self.specChanged.emit()
            self.signalPanelChanged.emit()

        def _update_settings(self, **changes: object) -> None:
            try:
                self._settings = self._settings.updated(**changes)
            except WrapperSettingsError as exc:
                self._ingest_synthetic_event(
                    "error",
                    {
                        "stage": "settings",
                        "error_type": "invalid_settings",
                        "message": str(exc),
                    },
                )
                return
            self._sync_effects_from_settings()
            self.effectsChanged.emit()

        def _sync_effects_from_settings(self) -> None:
            self._glow_enabled = self._settings.effect_enabled("glow")
            self._scanlines_enabled = self._settings.effect_enabled("scanlines")
            self._flicker_enabled = self._settings.effect_enabled("flicker")
            self._curvature_enabled = self._settings.effect_enabled("curvature")

        def _current_effects(self) -> dict[str, bool]:
            return {
                **self._settings.effect_map(),
                "glow": self._glow_enabled,
                "scanlines": self._scanlines_enabled,
                "flicker": self._flicker_enabled,
                "curvature": self._curvature_enabled,
            }

        def _persist_session_profile(self) -> None:
            if not self._options.restore_profile:
                return
            store = self._ensure_profile_store()
            if store is None:
                return
            try:
                store.save_current(
                    SESSION_PROFILE_NAME, self._settings, effects=self._current_effects()
                )
            except ProfileStoreError:
                pass

    return WrapperBridge


def _detect_caps_safely() -> RenderCapabilities | None:
    try:
        return detect_capabilities()
    except RenderCapsError:
        return None


def _settings_from_options(options: VisualWrapperOptions) -> WrapperSettings:
    return build_settings(
        theme_name=options.theme,
        effect_intensity=options.effect_intensity,
        font_family=options.font_family,
        font_scale=options.font_scale,
        reduced_effects=options.reduced_effects,
        plain_fallback=options.plain_fallback,
        rendering_mode=options.rendering_mode,
        quality_tier=options.quality_tier,
        font_width=options.font_width,
        line_spacing=options.line_spacing,
    )


def build_fixture_event_lines(
    project_path: str,
    start_command: str,
    max_iterations: int,
) -> list[str]:
    """Build deterministic fixture events for smoke tests and dry-run previews."""
    resolved_path = str(Path(project_path).expanduser())
    rows = [
        (
            "startup_begin",
            {"event_stream": True, "machine_output": True, "dry_run": True},
        ),
        (
            "config_loaded",
            {
                "config_path": "config.yaml",
                "provider_name": "ollama",
                "model_name": "qwen2.5-coder:7b-instruct-q4_K_M",
            },
        ),
        ("project_resolved", {"project_path": resolved_path}),
        (
            "spec_system_detected",
            {
                "project_path": resolved_path,
                "detected": True,
                "has_prd": True,
                "phase_count": 1,
                "latest_phase": "phase01",
            },
        ),
        (
            "autonomy_policy_resolved",
            {
                "dry_run": True,
                "max_iterations": max_iterations,
                "start_command": start_command,
                "risk_level": "low",
                "provider_preflight": True,
            },
        ),
        ("provider_check_started", {"provider_name": "ollama"}),
        (
            "provider_check_finished",
            {"provider_name": "ollama", "model_count": 3},
        ),
        (
            "startup",
            {
                "project_path": resolved_path,
                "provider_name": "ollama",
                "model_name": "qwen2.5-coder:7b-instruct-q4_K_M",
                "max_iterations": max_iterations,
                "dry_run": True,
                "start_command": start_command,
                "machine_output": True,
            },
        ),
        (
            "iteration_started",
            {
                "project_path": resolved_path,
                "provider_name": "ollama",
                "model_name": "qwen2.5-coder:7b-instruct-q4_K_M",
                "iteration": 1,
                "operation": "dry-run preview",
                "dry_run": True,
            },
        ),
        ("manager_decision_started", {"iteration": 1, "source": "fixture"}),
        (
            "manager_decision_finished",
            {
                "iteration": 1,
                "output": start_command,
                "reason": "Wrapper smoke fixture",
                "known_command": True,
            },
        ),
        ("task_progress", {"done": 4, "total": 12}),
        ("prompt_dispatched", {"iteration": 1, "prompt_length": 43}),
        (
            "codex_dry_run",
            {
                "binary": "codex",
                "project_path": resolved_path,
                "prompt_length": 43,
                "timeout_seconds": 1800,
            },
        ),
        ("artifact_detected", {"name": "session-spec.md"}),
        ("db_log_finished", {"project_path": project_path, "stored_state": "fixture"}),
        ("run_stopped", {"reason": "fixture_complete", "iteration": 1}),
    ]
    return [
        json.dumps(
            {
                "version": 1,
                "event": event,
                "timestamp": "2026-07-03T00:00:00Z",
                "payload": payload,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        for event, payload in rows
    ]


def parse_args(argv: list[str] | None = None) -> VisualWrapperOptions:
    """Parse wrapper command-line arguments."""
    parser = argparse.ArgumentParser(description="Apex Infinite visual wrapper")
    parser.add_argument("--path", default=os.getcwd(), help="Project path to display")
    parser.add_argument(
        "--start-command", default="implement", help="Optional start command"
    )
    parser.add_argument("--config", dest="config_path", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--launch-cli",
        action="store_true",
        help="Launch the real CLI instead of fixture playback",
    )
    parser.add_argument(
        "--theme",
        choices=list(WRAPPER_THEME_NAMES),
        default=THEME_CRT_GREEN,
    )
    parser.add_argument("--effect-intensity", type=int, default=None)
    parser.add_argument("--font-family", default="monospace")
    parser.add_argument("--font-scale", type=float, default=1.0)
    parser.add_argument("--font-width", type=float, default=1.0)
    parser.add_argument("--line-spacing", type=float, default=1.0)
    parser.add_argument(
        "--rendering-mode",
        choices=list(RENDERING_MODES),
        default=None,
        help="Rendering mode (default: theme preset default)",
    )
    parser.add_argument(
        "--quality-tier",
        choices=list(QUALITY_TIERS),
        default=DEFAULT_QUALITY_TIER,
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Load a saved visual profile by name at startup",
    )
    parser.add_argument(
        "--profile-store",
        dest="profile_store_path",
        default=None,
        help="Override the visual profile store path (testing/debug)",
    )
    parser.add_argument(
        "--no-restore-profile",
        action="store_true",
        help="Do not restore the last saved visual profile",
    )
    parser.add_argument(
        "--plain-fallback",
        action="store_true",
        help="Start with the plain low-effects fallback active",
    )
    parser.add_argument("--process-timeout-seconds", type=int, default=None)
    parser.add_argument("--reduced-effects", action="store_true")
    parser.add_argument("--auto-close-ms", type=int, default=None)
    args = parser.parse_args(argv)
    if args.max_iterations < 1:
        parser.error("--max-iterations must be positive")
    if args.auto_close_ms is not None and args.auto_close_ms < 1:
        parser.error("--auto-close-ms must be positive")
    if args.process_timeout_seconds is not None and args.process_timeout_seconds < 1:
        parser.error("--process-timeout-seconds must be positive")
    try:
        build_settings(
            theme_name=args.theme,
            effect_intensity=args.effect_intensity,
            font_family=args.font_family,
            font_scale=args.font_scale,
            reduced_effects=args.reduced_effects,
            plain_fallback=args.plain_fallback,
            rendering_mode=args.rendering_mode,
            quality_tier=args.quality_tier,
            font_width=args.font_width,
            line_spacing=args.line_spacing,
        )
    except WrapperSettingsError as exc:
        parser.error(str(exc))
    return VisualWrapperOptions(
        project_path=args.path,
        start_command=args.start_command,
        config_path=args.config_path,
        provider=args.provider,
        model=args.model,
        max_iterations=args.max_iterations,
        dry_run=args.dry_run,
        launch_cli=args.launch_cli,
        theme=args.theme,
        reduced_effects=args.reduced_effects,
        auto_close_ms=args.auto_close_ms,
        qml_path=Path(__file__).resolve().parent / "qml" / "Main.qml",
        effect_intensity=args.effect_intensity,
        font_family=args.font_family,
        font_scale=args.font_scale,
        plain_fallback=args.plain_fallback,
        process_timeout_seconds=args.process_timeout_seconds,
        rendering_mode=args.rendering_mode,
        quality_tier=args.quality_tier,
        font_width=args.font_width,
        line_spacing=args.line_spacing,
        profile=args.profile,
        restore_profile=not args.no_restore_profile,
        profile_store_path=args.profile_store_path,
    )


def run_app(options: VisualWrapperOptions) -> int:
    """Run the Qt Quick wrapper application."""
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        os.environ.setdefault("QT_QUICK_BACKEND", "software")
    qt = import_qt_modules()
    app = qt["QApplication"](sys.argv[:1])
    bridge_class = build_bridge_class(qt)
    bridge = bridge_class(options)
    engine = qt["QQmlApplicationEngine"]()
    context = engine.rootContext()
    context.setContextProperty("bridge", bridge)
    window_state = load_window_state() if options.restore_profile else {}
    context.setContextProperty(
        "initialWindowWidth", int(window_state.get("width", 1280))
    )
    context.setContextProperty(
        "initialWindowHeight", int(window_state.get("height", 800))
    )
    engine.load(qt["QUrl"].fromLocalFile(str(options.qml_path)))
    if not engine.rootObjects():
        raise VisualWrapperUnavailable("QML surface could not be loaded")
    app.aboutToQuit.connect(bridge.shutdown)
    if options.dry_run:
        qt["QTimer"].singleShot(0, bridge.startRun)
    auto_close_ms = options.auto_close_ms
    if auto_close_ms is None and os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        auto_close_ms = 900
    if auto_close_ms:
        qt["QTimer"].singleShot(auto_close_ms, app.quit)
    return app.exec()


def _format_log_line(entry) -> str:
    detail = f" - {entry.detail}" if entry.detail else ""
    return f"{entry.sequence:03d} [{entry.severity.upper()}] {entry.title}{detail}"


def _stderr_summary(stderr: str) -> str:
    stripped = stderr.strip()
    if not stripped:
        return "Base CLI wrote stderr."
    line_count = len(stripped.splitlines())
    return (
        f"Base CLI wrote {len(stripped)} stderr characters across {line_count} line(s)."
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for `apex-infinite-visual`."""
    try:
        return run_app(parse_args(argv))
    except VisualWrapperUnavailable as exc:
        print(f"Visual wrapper unavailable: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(
            "Visual wrapper unavailable: display backend or Qt runtime failed "
            f"({exc.__class__.__name__})",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
