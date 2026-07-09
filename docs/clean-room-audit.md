# Clean-Room Audit

**Session ID**: `phase00-session08-release-verification`
**Status**: Source-mode complete; binary release gated
**Last Updated**: 2026-07-09

---

## Boundary Summary

The `EXAMPLE/cool-retro-term/` tree is reference-only material. Product work may
use independent concepts such as terminal mood, status hierarchy, operator
controls, and effect categories. Product work must not copy reference source,
QML, shader code, compiled shader blobs, images, icons, fonts, profile data,
resource manifests, build scripts, GPL code, or terminal-emulator code.

Current tracked visual assets and shader sources are Apex-owned project files,
not imported reference files. Apex-owned tracked files may include SVG icon
assets, `.desktop` metadata, AppStream metadata, GLSL shader source, QML, tests,
docs, and packaging scripts when they were authored for this project and pass
the no-copy checks. Compiled `.qsb` files remain generated artifacts unless a
release explicitly promotes reviewed compiled outputs into package data.

---

## Audit Matrix

| Boundary | Evidence Task | Method | Status |
|----------|---------------|--------|--------|
| `EXAMPLE/` reference material is not tracked in product files. | T016 | `git ls-files` and path scan | PASS |
| Base CLI stays free of PySide6, Qt Quick, QML, and display-server imports. | T008, T018 | requirements and base CLI import scan | PASS |
| Wrapper dependencies stay optional and documented separately. | T008, T018 | `requirements-wrapper.txt` and docs audit | PASS |
| PySide6 LGPLv3/commercial obligations are documented before binary release. | T008, T017, T020 | wrapper productization docs and security posture audit | PASS; binary gated |
| Binary artifacts remain gated by packaging, checksum, notices, and source/relink evidence. | T008, T020 | release documentation and security posture audit | PASS; binary gated |
| No copied QML, shader, image, icon, font, profile data, resource manifest, build script, or GPL code was added. | T016 and Hyperterminal audit | tracked-file no-copy keyword, provenance, and path scans | PASS |
| Event stream and wrapper use raw JSONL/API facts, not scraped terminal frames. | T013, T017 | event smoke and docs audit | PASS |

---

## Boundary Confirmation

| Check | Result | Evidence |
|-------|--------|----------|
| Reference tree ignored | PASS | `.gitignore` contains `/EXAMPLE/`; local `EXAMPLE/cool-retro-term/` exists only as ignored reference material. |
| Forbidden-copy rules documented | PASS | `docs/visual-wrapper-boundary.md` defines forbidden source, QML, shader, asset, font, profile, resource, build-script, and terminal-emulator copying. |
| Optional dependency lane documented | PASS | `docs/visual-wrapper-productization.md` keeps `requirements-wrapper.txt` separate and says not to move PySide6 into `requirements.txt`. |
| License gates documented | PASS | Wrapper productization docs list LGPLv3/commercial review, notices, AppImage replacement/relink, source availability, and SHA256 gates. |
| Base CLI dependency boundary | PASS | Scan of `requirements.txt`, `src/apex_infinite/cli.py`, `src/apex_infinite/events.py`, and `src/apex_infinite/ui.py` found no PySide6, Qt Quick, QML, wrapper, or Nuitka references. |
| Security posture input | PASS | `docs/SECURITY-COMPLIANCE.md`, `docs/visual-wrapper-boundary.md`, `docs/visual-wrapper-productization.md`, and `packaging/NOTICES.md` record clean-room and optional wrapper findings that release verification must refresh. |

---

## Scans

Boundary confirmation completed in T004. Full tracked-file no-copy scans ran in
T016.

| Scan | Result | Evidence |
|------|--------|----------|
| Tracked `EXAMPLE/` paths | PASS | `git ls-files | grep '^EXAMPLE/' || true` produced no output. |
| Reference path/name scan | PASS | Tracked CLI/docs/workflow paths contain no reference asset, shader, generated shader blob, resource manifest, build script, terminal-widget, or copied QML names. |
| Binary/reference extension scan | PASS | Tracked Apex-owned `.frag`, `.desktop`, `.appdata.xml`, and `.svg` files are allowed release assets with provenance. No tracked `.qsb` files or `EXAMPLE/` paths are allowed. |
| Excluded component keyword scan | PASS | Hits are documentation of exclusions and backup options, not implementation imports or tracked copied material. |
| Base dependency/import scan | PASS | `requirements.txt`, `src/apex_infinite/cli.py`, `src/apex_infinite/events.py`, and `src/apex_infinite/ui.py` contain no PySide6, Qt, QML, or Nuitka references. |
| Dependency vulnerability audit | PASS | `pip-audit -r requirements.txt -r requirements-dev.txt -r requirements-wrapper.txt` reported no known vulnerabilities. |

---

## Wrapper Release-State Matrix

| Release Area | Source Evidence | Release Position | Verification Owner |
|--------------|-----------------|------------------|--------------------|
| Source wrapper entrypoint | `python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300` | Source-shippable; T011 smoke passed and T021 rerun passed | T011, T021 |
| QML lint | `pyside6-qmllint src/apex_infinite_visual/qml/Main.qml` | Source-shippable; lint exits 0 with known non-blocking warnings and T021 rerun passed | T011, T021 |
| Optional PySide6 import | `tests/test_visual_wrapper_productization.py` import-guard tests | Source-shippable; base import remains headless-safe | T009, T011, T018 |
| Guarded wrapper command | `build_apex_cli_command()` tests and launcher inspection | Source-shippable; wrapper uses `--event-stream - --machine-output` | T009, T013, T017 |
| Failure states | Productization tests for missing CLI, missing PySide6, malformed JSONL, timeout, stderr, non-zero exit, and stop | Source-shippable; tests passed | T009, T011 |
| Settings controls | Productization tests for theme, effect intensity, font family, font scale, reduced effects, and plain fallback | Source-shippable; tests passed | T009, T011 |
| Base dependency isolation | `requirements.txt` scan and base CLI import scan | Required for source and binary release | T018 |
| Optional dependency lane | `requirements-wrapper.txt` contains PySide6 and Nuitka only in wrapper lane | PASS for source wrapper; binary gate remains open | T018, T020 |
| PySide6/Qt license path | Wrapper docs list LGPLv3/commercial review and no GPL-only module checks | Binary-gated until legal/module review for an actual artifact | T020 |
| AppImage packaging | `scripts/build-appimage.sh` and `packaging/RELEASE-CHECKLIST.md` | Build script exists; clean-machine artifact verification remains gated | Release session |
| Checksums and notices | `packaging/NOTICES.md` and build-script checksum output | Notices exist; artifact checksum must be generated and verified for each release | Release session |
| Source/relink obligations | `packaging/NOTICES.md` and venv-in-AppDir packaging decision | Documented for current intended bundle shape; verify against concrete artifact | Release session |

---

## Release Position

The tracked source and documentation pass the clean-room release checks run in
T004, T016, T017, T018, and T020. The base terminal CLI remains independent of
PySide6, Qt Quick, QML, Nuitka, wrapper assets, and display-server requirements.

The optional PySide6/QML wrapper source mode is source-shippable. The
repository includes original visual assets, clean-room shader sources, desktop
metadata, AppStream metadata, notices, a release checklist, and an AppImage
build script. Binary publication remains gated until a release session
completes generated-bundle review, license/module review, dependency
inventory, checksum verification, source/relink verification, and
clean-machine launch evidence for the concrete artifact.
