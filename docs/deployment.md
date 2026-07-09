# Deployment

This repository does not deploy a hosted service. For guarded live operation
of the source-shippable base CLI, use `make production PROJECT=/absolute/path`
as documented in the operator runbook. That target performs local readiness
checks and starts the operator process; it is not an infrastructure deployment.

## Local Dev

Create the repository environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev,visual]"
```

Run a smoke-oriented dry run:

```bash
.venv/bin/apex-infinite --path "$PWD" --start plansession --dry-run --max-iterations 1
```

Stop local Ollama when it is no longer needed:

```bash
./scripts/ollama-docker.sh down
```

## CI/CD Pipeline

The repository defines one GitHub Actions workflow at
`.github/workflows/quality.yml`. It runs on `push` and `pull_request`, installs
the package with the `dev` extra on Python 3.10, and runs:

```bash
python -m black --check src tests
python -m pylint src/apex_infinite src/apex_infinite_visual
python -m mypy
```

The workflow does not publish packages, create releases, deploy services, run
dependency audits, or build visual-wrapper binaries.

## Release Artifact Build

Local release verification builds source and wheel artifacts outside the
repository:

```bash
.venv/bin/python -m build --outdir /tmp/apex-infinite-cli-smoke-dist
```

Use the full release smoke matrix in
[Operator runbook](operator-runbook.md#local-release-smoke-procedure) before a
public release.

## Visual AppImage Release

The first binary visual-wrapper artifact is:

```text
apex-infinite-visual-linux-x86_64.AppImage
```

Build it only in a release session:

```bash
scripts/build-appimage.sh
```

Before publishing, inspect the AppDir contents, bundled PySide6/Qt modules,
QML resources, shader artifacts, dependency inventory, notices, and checksum.
Verify the AppImage on a clean supported Linux machine that does not have this
repository or its `.venv`.

The current AppImage path uses a venv-in-AppDir bundle rather than compiling
the Python application with Nuitka. This keeps the bundled PyPI wheels
byte-auditable and keeps the Qt/PySide6 LGPL replacement/relink path explicit.

## Release And Rollback

- Release: manual. Build artifacts with `python -m build`, review smoke
  evidence, and publish through an external packaging process if one is chosen.
- Rollback: manual. Reinstall a known-good build or commit through the target
  environment's package process. No automated rollback workflow is present.
- Optional visual-wrapper binary release: gated. Future binary publication must
  complete generated-bundle review, license/module review, notices, checksum,
  dependency inventory, clean-machine launch evidence, and source/relink
  instructions.

## Operational Gates

- Do not publish real event streams, local history DBs, provider keys, or smoke
  homes from `/tmp`.
- Keep PySide6 and graphical dependencies out of the base CLI install.
- Re-run dependency audit before release or dependency changes.
