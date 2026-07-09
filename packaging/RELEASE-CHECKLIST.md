# Hyperterminal Release Checklist

Run every gate before shipping a visual release artifact.

## Packaging Decision Record

`pyside6-deploy` (Nuitka-based) was evaluated first per the design plan.
The venv-in-AppDir approach in `scripts/build-appimage.sh` was chosen
instead because:

- It keeps the bundle byte-auditable: the AppDir contains unmodified PyPI
  wheels plus this project's wheel, which makes the LGPL relink path
  trivial (swap wheels, repack).
- Nuitka compilation obscures the Python/QML boundary and complicates the
  clean-room review of what ships.
- Startup time is dominated by Qt initialization either way.

Revisit if binary-size or cold-start budgets change.

## Quality Gates

- [ ] `.venv/bin/python -m pytest tests/ -v`
- [ ] `.venv/bin/python -m black --check src tests`
- [ ] `.venv/bin/python -m mypy`
- [ ] `.venv/bin/python -m pylint src/apex_infinite src/apex_infinite_visual`
- [ ] `QT_QPA_PLATFORM=offscreen .venv/bin/python -m apex_infinite_visual --dry-run --auto-close-ms 1500 --no-restore-profile`
- [ ] `python scripts/visual_screenshot_smoke.py --theme apex-reactor --out /tmp/smoke-high.png`
- [ ] `python scripts/visual_screenshot_smoke.py --theme crt-green --out /tmp/smoke-balanced.png`
- [ ] `python scripts/visual_screenshot_smoke.py --theme blackbox --out /tmp/smoke-low.png`
- [ ] `python scripts/visual_screenshot_smoke.py --theme plain --out /tmp/smoke-plain.png`

## Clean-Room / License Gates

- [ ] `git ls-files | grep '^EXAMPLE/'` returns nothing.
- [ ] `git diff --check` is clean.
- [ ] No `.qsb`, image, font, or profile file in the diff originates from
      the reference tree; shader artifacts were regenerated from
      `src/apex_infinite_visual/shaders/` via `scripts/build-shaders.sh`
      and reviewed.
- [ ] `packaging/NOTICES.md` matches the bundled dependency inventory.
- [ ] No GPL-only Qt modules appear in `dependency-inventory.txt`.

## Base CLI Isolation

- [ ] Fresh venv, `pip install .` (no extras), then
      `python -c "import PySide6"` fails and `apex-infinite --help` works.

## AppImage

- [ ] `scripts/build-appimage.sh` completes.
- [ ] `sha256sum -c apex-infinite-visual-linux-x86_64.AppImage.sha256` passes.
- [ ] AppImage launches on a clean machine without this repo or `.venv`:
      `./apex-infinite-visual-linux-x86_64.AppImage --dry-run --auto-close-ms 2000`
- [ ] Missing Codex/provider config produces the visual failure state, not
      a crash (`--launch-cli` against an empty project).
- [ ] Desktop entry validates: `desktop-file-validate src/apex_infinite_visual/assets/apex-infinite-visual.desktop`
- [ ] AppStream validates: `appstreamcli validate src/apex_infinite_visual/assets/apex-infinite-visual.appdata.xml`
