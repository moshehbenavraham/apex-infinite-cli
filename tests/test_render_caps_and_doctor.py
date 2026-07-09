"""Render capability detection and visual doctor tests."""

import pytest

from apex_infinite_visual.doctor import (
    DOCTOR_FAIL,
    DOCTOR_PASS,
    DOCTOR_WARN,
    DoctorContext,
    doctor_event_rows,
    run_doctor,
)
from apex_infinite_visual.render_caps import (
    BACKEND_HARDWARE,
    BACKEND_SOFTWARE,
    FORCE_TIER_ENV,
    RenderCapsError,
    capabilities_payload,
    detect_capabilities,
    resolve_quality_tier,
)

DESKTOP_ENV = {"DISPLAY": ":0"}


def test_offscreen_platform_forces_low_effects_software_backend():
    caps = detect_capabilities(env={"QT_QPA_PLATFORM": "offscreen"})

    assert caps.offscreen is True
    assert caps.backend == BACKEND_SOFTWARE
    assert caps.recommended_tier == "low-effects"
    assert caps.reduced_effects_forced is True
    assert caps.shaders_available is False


def test_software_quick_backend_recommends_battery():
    caps = detect_capabilities(env={"QT_QUICK_BACKEND": "software"})

    assert caps.backend == BACKEND_SOFTWARE
    assert caps.recommended_tier == "battery"


def test_hardware_without_shaders_recommends_balanced(tmp_path):
    caps = detect_capabilities(env=DESKTOP_ENV, shader_dir=tmp_path)

    assert caps.backend == BACKEND_HARDWARE
    assert caps.shaders_available is False
    assert caps.recommended_tier == "balanced"


def test_hardware_with_compiled_shaders_recommends_cinematic(tmp_path):
    (tmp_path / "surface_postprocess.frag.qsb").write_bytes(b"qsb")

    caps = detect_capabilities(env=DESKTOP_ENV, shader_dir=tmp_path)

    assert caps.shaders_available is True
    assert caps.shader_modules == ("surface_postprocess",)
    assert caps.recommended_tier == "cinematic"


def test_forced_tier_env_override_and_validation(tmp_path):
    caps = detect_capabilities(
        env={FORCE_TIER_ENV: "battery", "DISPLAY": ":0"}, shader_dir=tmp_path
    )
    assert caps.recommended_tier == "battery"
    assert resolve_quality_tier("cinematic", caps) == "battery"

    with pytest.raises(RenderCapsError, match="must be one of"):
        detect_capabilities(env={FORCE_TIER_ENV: "ultra"})


def test_resolve_quality_tier_clamps_to_recommendation(tmp_path):
    caps = detect_capabilities(env={"QT_QPA_PLATFORM": "offscreen"})

    assert resolve_quality_tier("cinematic", caps) == "low-effects"
    assert resolve_quality_tier("plain", caps) == "plain"
    with pytest.raises(RenderCapsError):
        resolve_quality_tier("nope", caps)


def test_capabilities_payload_is_event_safe(tmp_path):
    caps = detect_capabilities(env=DESKTOP_ENV, shader_dir=tmp_path)
    payload = capabilities_payload(caps)

    assert payload["quality_tier"] == "balanced"
    assert isinstance(payload["shader_modules"], list)
    assert set(payload) == {
        "platform",
        "backend",
        "offscreen",
        "shaders_available",
        "shader_modules",
        "quality_tier",
        "reduced_effects_forced",
    }


def make_context(tmp_path, **overrides):
    """Build a doctor context with hermetic defaults."""
    project = tmp_path / "project"
    project.mkdir(exist_ok=True)
    defaults = {
        "project_path": str(project),
        "config_path": "",
        "codex_binary": "codex",
        "env": {"DISPLAY": ":0"},
        "which": lambda _name: "/usr/bin/codex",
        "module_available": lambda _name: True,
    }
    defaults.update(overrides)
    return DoctorContext(**defaults)


def test_doctor_all_green_is_launch_ready(tmp_path):
    report = run_doctor(make_context(tmp_path))

    assert report.launch_ready is True
    assert report.counts()[DOCTOR_FAIL] == 0
    assert {check.check_id for check in report.checks} == {
        "config",
        "project",
        "codex",
        "history",
        "pyside6",
        "display",
    }


def test_doctor_missing_codex_and_project_fail(tmp_path):
    context = make_context(
        tmp_path,
        project_path=str(tmp_path / "missing"),
        which=lambda _name: None,
    )
    report = run_doctor(context)

    by_id = {check.check_id: check for check in report.checks}
    assert by_id["codex"].status == DOCTOR_FAIL
    assert by_id["project"].status == DOCTOR_FAIL
    assert report.launch_ready is False
    assert report.status == DOCTOR_FAIL


def test_doctor_missing_pyside6_fails_and_offscreen_warns(tmp_path):
    context = make_context(
        tmp_path,
        env={"QT_QPA_PLATFORM": "offscreen"},
        module_available=lambda _name: False,
    )
    report = run_doctor(context)

    by_id = {check.check_id: check for check in report.checks}
    assert by_id["pyside6"].status == DOCTOR_FAIL
    assert by_id["display"].status == DOCTOR_WARN


def test_doctor_missing_display_fails(tmp_path):
    report = run_doctor(make_context(tmp_path, env={}))

    by_id = {check.check_id: check for check in report.checks}
    assert by_id["display"].status == DOCTOR_FAIL


def test_doctor_explicit_config_path(tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("provider: ollama\n", encoding="ascii")

    report = run_doctor(make_context(tmp_path, config_path=str(config)))
    by_id = {check.check_id: check for check in report.checks}
    assert by_id["config"].status == DOCTOR_PASS

    report = run_doctor(make_context(tmp_path, config_path=str(tmp_path / "nope.yaml")))
    by_id = {check.check_id: check for check in report.checks}
    assert by_id["config"].status == DOCTOR_FAIL


def test_doctor_event_rows_are_display_safe(tmp_path):
    report = run_doctor(make_context(tmp_path))
    rows = doctor_event_rows(report)

    assert len(rows) == len(report.checks)
    for row in rows:
        assert set(row) == {"check_id", "label", "status", "detail"}
        assert row["status"] in {DOCTOR_PASS, DOCTOR_WARN, DOCTOR_FAIL}
