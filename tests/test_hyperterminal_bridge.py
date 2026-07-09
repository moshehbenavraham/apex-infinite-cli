"""Hyperterminal bridge tests for doctor, profiles, filters, and pulses."""

import json
from pathlib import Path

from apex_infinite_visual import main as visual_main
from apex_infinite_visual.main import (
    VisualWrapperOptions,
    build_bridge_class,
    build_fixture_event_lines,
    parse_args,
)
from apex_infinite_visual.render_caps import (
    BACKEND_HARDWARE,
    BACKEND_SOFTWARE,
    RenderCapabilities,
)


class FakeSignal:
    """Signal double for bridge tests."""

    def __init__(self, *_types):
        self.callbacks = []

    def connect(self, callback):
        """Register one callback."""
        self.callbacks.append(callback)

    def emit(self, *args):
        """Invoke registered callbacks."""
        for callback in self.callbacks:
            callback(*args)


class FakeQObject:
    """QObject double for bridge tests."""

    def __init__(self, *_args, **_kwargs):
        super().__init__()


class FakeTimer:
    """Timer double for bridge tests."""

    def __init__(self, *_args, **_kwargs):
        self.timeout = FakeSignal()
        self.active = False

    def setInterval(self, _interval):
        """Ignore the interval."""

    def start(self):
        """Mark the timer active."""
        self.active = True

    def stop(self):
        """Mark the timer inactive."""
        self.active = False

    def isActive(self):
        """Return whether the timer is active."""
        return self.active


def fake_property(_kind, getter, notify=None):  # pylint: disable=unused-argument
    """Return a Python property for fake bridge tests."""
    return property(getter)


def fake_slot(*_args, **_kwargs):
    """Return an identity decorator for fake bridge tests."""

    def decorator(func):
        return func

    return decorator


def fake_qt_modules():
    """Return fake Qt bindings for bridge tests."""
    return {
        "Property": fake_property,
        "QObject": FakeQObject,
        "QTimer": FakeTimer,
        "Signal": FakeSignal,
        "Slot": fake_slot,
    }


def bridge_options(tmp_path, **overrides):
    """Build hyperterminal bridge options."""
    values = {
        "project_path": str(tmp_path),
        "start_command": "implement",
        "config_path": None,
        "provider": None,
        "model": None,
        "max_iterations": 3,
        "dry_run": True,
        "launch_cli": False,
        "theme": "apex-reactor",
        "reduced_effects": False,
        "auto_close_ms": None,
        "qml_path": tmp_path / "Main.qml",
        "effect_intensity": 70,
        "quality_tier": "balanced",
        "profile_store_path": str(tmp_path / "profiles.json"),
    }
    values.update(overrides)
    return VisualWrapperOptions(**values)


def make_bridge(tmp_path, **overrides):
    """Build a bridge with fake Qt modules."""
    bridge_class = build_bridge_class(fake_qt_modules())
    return bridge_class(bridge_options(tmp_path, **overrides))


def render_caps(recommended_tier, backend=BACKEND_HARDWARE, offscreen=False):
    """Build deterministic render capabilities for bridge tests."""
    return RenderCapabilities(
        platform="offscreen" if offscreen else "xcb",
        backend=backend,
        offscreen=offscreen,
        shaders_available=backend == BACKEND_HARDWARE,
        shader_modules=("surface_postprocess",),
        recommended_tier=recommended_tier,
        reduced_effects_forced=recommended_tier in {"low-effects", "plain"},
    )


def run_fixture(bridge):
    """Drive the fixture playback to completion."""
    bridge.startRun()
    while bridge._fixture_timer.isActive():  # pylint: disable=protected-access
        bridge._emit_next_fixture()  # pylint: disable=protected-access


def test_fixture_flow_populates_spec_map_and_signal_panel(tmp_path):
    bridge = make_bridge(tmp_path)
    run_fixture(bridge)

    assert bridge.specDetected is True
    assert "phase01" in bridge.specPhase
    assert bridge.taskProgressText == "4 / 12"
    assert bridge.taskProgressRatio > 0.3
    assert bridge.providerHealth == "ok"
    assert bridge.artifacts == ["session-spec.md"]
    assert bridge.specCommand == "implement"
    assert bridge.runHealth == "stopped"


def test_capabilities_event_is_ingested_at_startup(tmp_path):
    bridge = make_bridge(tmp_path)

    rows = bridge.eventRows
    assert rows
    assert rows[0]["event"] == "wrapper_capabilities_resolved"
    assert bridge.backendName in {"hardware", "software"}
    assert bridge.recommendedTier in bridge.qualityTiers


def test_event_filters_and_search(tmp_path):
    bridge = make_bridge(tmp_path)
    run_fixture(bridge)
    total = len(bridge.eventRows)

    bridge.setStageFilter("preflight")
    assert 0 < len(bridge.eventRows) < total
    assert all(row["stage"] == "preflight" for row in bridge.eventRows)

    bridge.setStageFilter("")
    bridge.setSeverityFilter("success")
    assert all(row["severity"] == "success" for row in bridge.eventRows)

    bridge.setSeverityFilter("")
    bridge.setSearchText("codex")
    assert bridge.eventRows
    assert all(
        "codex" in f"{row['title']} {row['detail']} {row['event']}".lower()
        for row in bridge.eventRows
    )


def test_pulses_are_drained_to_pulse_names(tmp_path):
    bridge = make_bridge(tmp_path)
    seen = []
    bridge.pulsesChanged.connect(lambda: seen.extend(bridge.pulseNames))
    run_fixture(bridge)

    assert "surface_charge" in seen
    assert "signal_sweep" in seen
    assert "decision_pulse" in seen


def test_run_doctor_publishes_rows_and_events(tmp_path):
    bridge = make_bridge(tmp_path)
    bridge.runDoctor()

    assert len(bridge.doctorRows) == 6
    assert bridge.doctorStatus in {"pass", "warn", "fail"}
    events = [row["event"] for row in bridge.eventRows]
    assert "doctor_started" in events
    assert "doctor_finished" in events
    assert events.count("doctor_check") == 6


def test_profile_save_load_delete_round_trip(tmp_path):
    bridge = make_bridge(tmp_path)
    bridge.setEffectIntensity(90)
    bridge.saveProfile("night-shift")

    assert bridge.profileError == ""
    assert "night-shift" in bridge.profileNames

    bridge.setEffectIntensity(20)
    bridge.loadProfile("night-shift")
    assert bridge.effectIntensity == 90
    assert bridge.activeProfile == "night-shift"

    bridge.loadProfile("blackbox")
    assert bridge.themeName == "blackbox"

    bridge.deleteProfile("night-shift")
    assert "night-shift" not in bridge.profileNames

    bridge.deleteProfile("crt-green")
    assert "custom" in bridge.profileError


def test_profile_restore_at_startup(tmp_path):
    first = make_bridge(tmp_path)
    first.setTheme("incident-red")
    first.saveProfile("ops")

    second = make_bridge(tmp_path, restore_profile=True)
    assert second.activeProfile == "ops"
    assert second.themeName == "incident-red"


def test_profile_restore_reapplies_capability_clamps(tmp_path, monkeypatch):
    monkeypatch.setattr(
        visual_main,
        "_detect_caps_safely",
        lambda: render_caps("cinematic"),
    )
    first = make_bridge(tmp_path)
    first.setQualityTier("cinematic")
    first.saveProfile("ops")

    monkeypatch.setattr(
        visual_main,
        "_detect_caps_safely",
        lambda: render_caps("low-effects", backend=BACKEND_SOFTWARE, offscreen=True),
    )
    second = make_bridge(tmp_path, restore_profile=True)

    assert second.activeProfile == "ops"
    assert second.qualityTier == "low-effects"
    assert second.effectiveQualityTier == "low-effects"
    assert second.reducedEffects is True
    assert second.effectFps == 12


def test_profile_save_load_preserves_manual_effect_toggles(tmp_path):
    bridge = make_bridge(tmp_path)

    bridge.setEffectEnabled("glow", False)
    bridge.saveProfile("manual-effects")

    payload = json.loads((tmp_path / "profiles.json").read_text(encoding="ascii"))
    profile = next(
        entry for entry in payload["profiles"] if entry["name"] == "manual-effects"
    )
    assert profile["effects"]["glow"] is False

    bridge.setEffectEnabled("glow", True)
    assert bridge.glowEnabled is True

    bridge.loadProfile("manual-effects")

    assert bridge.profileError == ""
    assert bridge.glowEnabled is False


def test_quality_tier_slot_validates_and_updates(tmp_path):
    bridge = make_bridge(tmp_path)
    bridge.setQualityTier("battery")

    assert bridge.qualityTier == "battery"
    assert bridge.effectFps == 24

    bridge.setRenderingMode("cinematic")
    assert bridge.renderingMode == "cinematic"

    bridge.setRenderingMode("bogus")
    assert bridge.hasError is True


def test_export_events_writes_json(tmp_path):
    bridge = make_bridge(tmp_path)
    run_fixture(bridge)
    target = tmp_path / "export" / "events.json"

    bridge.exportEvents(str(target))

    rows = json.loads(target.read_text(encoding="ascii"))
    assert isinstance(rows, list)
    assert any(row["event"] == "run_stopped" for row in rows)


def test_autonomy_summary_tracks_dry_run(tmp_path):
    bridge = make_bridge(tmp_path)
    assert "DRY RUN" in bridge.autonomySummary

    bridge.setDryRun(False)
    assert "LIVE" in bridge.autonomySummary
    assert "elevated" in bridge.autonomySummary


def test_parse_args_accepts_hyperterminal_flags(tmp_path):
    options = parse_args(
        [
            "--theme",
            "apex-reactor",
            "--rendering-mode",
            "cinematic",
            "--quality-tier",
            "cinematic",
            "--font-width",
            "1.1",
            "--line-spacing",
            "1.2",
            "--profile-store",
            str(tmp_path / "p.json"),
            "--no-restore-profile",
        ]
    )

    assert options.rendering_mode == "cinematic"
    assert options.quality_tier == "cinematic"
    assert options.font_width == 1.1
    assert options.line_spacing == 1.2
    assert options.restore_profile is False
    assert options.profile_store_path == str(tmp_path / "p.json")


def test_fixture_lines_all_use_registered_events():
    lines = build_fixture_event_lines("/tmp/project", "implement", 2)

    for line in lines:
        row = json.loads(line)
        assert row["version"] == 1
        assert row["event"]
        assert isinstance(row["payload"], dict)


def test_session_profile_persisted_on_shutdown(tmp_path):
    bridge = make_bridge(tmp_path, restore_profile=True)
    bridge.setTheme("blueprint-dos")
    bridge.shutdown()

    reopened = make_bridge(tmp_path, restore_profile=True)
    assert reopened.themeName == "blueprint-dos"
    assert reopened.activeProfile == "last-session"
