# Terminal Install Guide

Installed-user paths for the base `apex-infinite` terminal CLI. The base
install is terminal-only: it never installs PySide6, Nuitka, or QML assets
and never requires a display server. The visual wrapper is a separate
opt-in extra (`.[visual]`).

## pipx (recommended for operators)

```bash
cd apex-infinite-cli
pipx install .
```

`pipx` creates an isolated venv and exposes `apex-infinite` on your shell
path (usually via `~/.local/bin/apex-infinite`). Verify:

```bash
apex-infinite --version
apex-infinite --help
apex-infinite --check-provider
```

Upgrade after pulling new source:

```bash
pipx install . --force
```

Uninstall:

```bash
pipx uninstall apex-infinite-cli
```

## From built wheel or sdist

Build the artifacts (or download them from a release):

```bash
python -m build --outdir dist/
```

Install the wheel into any clean venv:

```bash
python3 -m venv ~/.venvs/apex-infinite
~/.venvs/apex-infinite/bin/python -m pip install dist/apex_infinite_cli-*.whl
```

Or install the sdist the same way:

```bash
~/.venvs/apex-infinite/bin/python -m pip install dist/apex_infinite_cli-*.tar.gz
```

## Dedicated local venv on the shell path

For a plain-venv install that exposes `apex-infinite` without activating
the repo `.venv`:

```bash
python3 -m venv ~/.venvs/apex-infinite
~/.venvs/apex-infinite/bin/python -m pip install /path/to/apex-infinite-cli
ln -s ~/.venvs/apex-infinite/bin/apex-infinite ~/.local/bin/apex-infinite
```

(`~/.local/bin` must be on `PATH`; most distributions add it by default.)

Upgrade: rerun the `pip install` with `--upgrade` (or against the new
wheel). Uninstall: remove the symlink and delete `~/.venvs/apex-infinite`.

## Verify any install

```bash
apex-infinite --version          # prints the installed version
apex-infinite --help             # lists every root flag
apex-infinite --doctor           # full readiness diagnostics
apex-infinite --check-provider   # provider connectivity + model preflight
```

The base install must not be able to import PySide6:

```bash
python -c "import PySide6" && echo "UNEXPECTED: visual extra leaked" \
  || echo "OK: base install is terminal-only"
```

## First run

```bash
apex-infinite --setup    # interactive; writes the XDG shared config
apex-infinite --doctor   # verify provider, Codex, project, history readiness
apex-infinite --path /path/to/project --dry-run
```

Always make the first execution against a new project a `--dry-run`.

## Config resolution

The CLI resolves its config through a fixed chain (first match wins):

1. `--config /path/to/config.yaml`
2. `APEX_INFINITE_CONFIG=/path/to/config.yaml`
3. `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/config.yaml` (written by
   `--setup`)
4. `./config.yaml` in the working directory
5. `config.yaml` at the source checkout root (development only)
6. Packaged defaults inside the installed package

The resolved path and its source category are shown in the startup panel
and emitted as the `config_resolved` event. A `.env` file next to the
selected config file overrides a `.env` in the working directory.

## Common shortcuts

Shell aliases for frequent starts:

```bash
alias apex-dry='apex-infinite --dry-run'
alias apex-resume='apex-infinite'          # default project comes from config
alias apex-history='apex-infinite --history'
alias apex-check='apex-infinite --check-provider'
alias apex-plain='apex-infinite --plain'
```

Resume pattern: history lives in SQLite keyed by project path, and the
manager summarizes it on every run, so "resume" is simply re-running
`apex-infinite` against the same project. With `defaults.project` set in
the shared config (via `--setup --default-project ...`), a bare
`apex-infinite` resumes the configured project.

## Uninstall data cleanup

Removing the package does not delete operator data. To remove everything:

```bash
apex-infinite --purge-history --yes            # or delete ~/.apex-infinite/
rm -rf ~/.config/apex-infinite                 # shared config (+ backups)
rm -rf ~/.local/state/apex-infinite            # notice marker, wrapper state, run logs
```
