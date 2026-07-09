# Apex Infinite CLI Operator Runbook

## Purpose

This runbook is for humans operating `apex-infinite` against a real project.
It assumes the CLI, config, and Codex skill are already installed.

## Prerequisites

- Python 3.10+
- Codex CLI installed and available as `codex`, or a custom `codex.binary`
- A valid `config.yaml`
- Required API keys exported through `.env` or the shell environment
- A target project directory that Codex can access

## Startup Checklist

Before the first run:

0. On a fresh machine, run `apex-infinite --setup` to write the shared
   config, then `apex-infinite --doctor` to verify Python, config, Codex,
   provider, project, and history readiness in one pass. Doctor exits
   non-zero on blockers and prints a fix command per failing row.
1. Confirm the target `--path` is the project you want Codex to modify.
2. Confirm the resolved config points at the intended provider and model.
   Resolution order: `--config`, `APEX_INFINITE_CONFIG`, the XDG shared
   config written by `--setup`, `./config.yaml`, the source checkout root,
   then packaged defaults. The startup panel shows the resolved path and
   source category.
3. Confirm `codex.binary` resolves to the intended Codex CLI executable.
4. Confirm `codex.exec_flags` matches the autonomy level you want. The
   packaged default is `--dangerously-bypass-approvals-and-sandbox`, which
   bypasses approvals and sandboxing and should be used only in an externally
   controlled workspace.
5. Confirm `codex.model_reasoning_effort` is one of `minimal`, `low`,
   `medium`, `high`, or `xhigh`. The value is passed to Codex as
   `-c model_reasoning_effort="<value>"`.
6. Run `apex-infinite --check-provider` or
   `scripts/check-ollama.sh --chat` for local Ollama.
7. Verify the target project already has the Apex Spec skill available if the
   run depends on `apex-spec` workflow commands.
8. Decide whether you want a forced starting command with `--start` or manager
   auto-selection from the first iteration.
9. Decide whether you want the first instruction seeded with `--ceo`.
10. Decide which display mode fits the terminal: styled interactive output,
   plain logs, ASCII-safe output, compact output, or machine-output JSONL.

## Common Run Modes

### Interactive selection

```bash
cd apex-infinite-cli
apex-infinite
```

Use this when you want the CLI to list directories under `~/projects/` and
prompt for the project, start command, and optional CEO instruction.

### Direct execution

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --start plansession
```

Use this when the target path and first command are already known.

### Guarded production-like local execution

```bash
cd apex-infinite-cli
make production \
  PROJECT=/absolute/path/to/initialized-apex-spec-project \
  START=plansession
```

This is the primary serious local operator target. It is intentionally stricter
than a direct invocation: `PROJECT` must be absolute, exist, and contain
`.spec_system`; the XDG shared config and repository virtualenv executable must
already exist; and launch-time installation is forbidden. Run
`.venv/bin/apex-infinite --setup` first when the shared config is absent.

The launcher writes separate `preflight-<utc>-<pid>.jsonl` and
`run-<utc>-<pid>.jsonl` files, runs terminal doctor plus a provider chat check,
and only then starts live autonomous execution. It does not pass `--dry-run`,
`--skip-provider-check`, or `--machine-output`. The default safety cap is 50
iterations.

Optional Make variables are:

```text
CONFIG=/absolute/path/to/config.yaml
START=plansession
MAX_ITERATIONS=25
LOG_DIR=/absolute/path/to/private-logs
```

Omit `START` when resuming and allowing the manager to select the next action
from stored history. A `START` value overrides only the first iteration. The
default log directory is
`${XDG_STATE_HOME:-~/.local/state}/apex-infinite/logs/`; there is no automatic
rotation, so include these files in the operator's retention procedure.

This target is production-like source operation, not a hosted deployment.
The default broad-autonomy Codex flags remain suitable only for an externally
controlled and recoverable workspace.

### Provider preflight

```bash
cd apex-infinite-cli
apex-infinite --check-provider
apex-infinite --check-provider --check-provider-chat
scripts/check-ollama.sh --chat
```

Use this before unattended runs. Normal runs execute the model-list preflight
before the loop starts; `--check-provider-chat` adds a tiny chat completion.
Use `--skip-provider-check` only for intentional offline wiring checks.

### Local release smoke procedure

Use this procedure before release verification or after a smoke-remediation
session. It avoids stale activated virtualenvs and keeps generated evidence
outside the repository.

1. Start from the repository root and inspect the active shell Python:

   ```bash
   cd apex-infinite-cli
   python -c 'import sys; print(sys.executable)'
   python -m pip --version
   ```

2. If either path points outside this repository, deactivate that environment
   or open a fresh shell. Create a repository venv explicitly:

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -e ".[dev,visual]"
   ```

3. Record the runtime identity:

   ```bash
   .venv/bin/python --version
   .venv/bin/python -c 'import sys; print(sys.executable)'
   .venv/bin/python -m pip --version
   codex --version
   .venv/bin/apex-infinite --version
   ```

4. Prepare isolated artifacts:

   ```bash
   rm -rf /tmp/apex-infinite-cli-smoke-home \
     /tmp/apex-infinite-cli-smoke-wrapper-home \
     /tmp/apex-infinite-cli-smoke-real-home \
     /tmp/apex-infinite-cli-smoke-dist
   rm -f /tmp/apex-infinite-smoke-events.jsonl \
     /tmp/apex-infinite-smoke-machine-output.jsonl \
     /tmp/apex-infinite-smoke-real-codex-events.jsonl \
     /tmp/apex-infinite-smoke-wrapper-events.jsonl
   mkdir -p /tmp/apex-infinite-cli-smoke-home \
     /tmp/apex-infinite-cli-smoke-wrapper-home \
     /tmp/apex-infinite-cli-smoke-real-home \
     /tmp/apex-infinite-cli-smoke-dist
   ```

5. Run quality checks through the venv Python:

   ```bash
   .venv/bin/python -m pytest tests/ -v
   .venv/bin/python -m black --check src tests
   .venv/bin/python -m mypy
   .venv/bin/python -m pylint src tests
   .venv/bin/python -m pip_audit
   .venv/bin/python -m build --outdir /tmp/apex-infinite-cli-smoke-dist
   ```

6. Verify provider and runtime smoke paths with temporary history and event
   files:

   ```bash
   ./scripts/check-ollama.sh --chat
   HOME=/tmp/apex-infinite-cli-smoke-home \
     .venv/bin/apex-infinite --provider ollama --check-provider \
     --check-provider-chat
   HOME=/tmp/apex-infinite-cli-smoke-home \
     .venv/bin/apex-infinite --path "$PWD" --start plansession \
     --dry-run --max-iterations 1 \
     --event-stream /tmp/apex-infinite-smoke-events.jsonl
   HOME=/tmp/apex-infinite-cli-smoke-home \
     .venv/bin/apex-infinite --path "$PWD" --start plansession \
     --dry-run --max-iterations 1 \
     --event-stream - --machine-output \
     > /tmp/apex-infinite-smoke-machine-output.jsonl
   ```

7. Run wrapper checks only from the visual extra environment:

   ```bash
   QT_QPA_PLATFORM=offscreen HOME=/tmp/apex-infinite-cli-smoke-wrapper-home \
     .venv/bin/apex-infinite-visual --dry-run --max-iterations 1 \
     --auto-close-ms 900
   QT_QPA_PLATFORM=offscreen HOME=/tmp/apex-infinite-cli-smoke-wrapper-home \
     .venv/bin/apex-infinite-visual --launch-cli --path "$PWD" \
     --start-command plansession --dry-run --max-iterations 1 \
     --auto-close-ms 1500
   ```

8. Run actual nested Codex smoke only with a no-edit prompt, a bounded
   one-iteration run, and `git status --short` before and after. Record the
   event path and confirm the tracked worktree did not gain unintended source
   changes.

If local Ollama is unavailable, use a configured equivalent provider only after
recording the provider name, model, base URL category, and reason for
substitution in the smoke report. Do not record provider secrets, full config
maps, or API keys.

### Dry run

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --start plansession --dry-run
```

Use this before changing providers, models, Codex flags, or reasoning effort.
It exercises the manager loop and prints the effective `codex exec` command,
including quoted `exec_flags` values and the `-c model_reasoning_effort`
override, without launching Codex. For non-dry-run starts, the CLI parses
configured `codex.exec_flags`, rejects malformed quoting or unsupported
reasoning effort, and checks flags against local `codex exec --help` after
resolving the project path and before the autonomous loop begins. If a flag is
stale, update the config or keep using dry-run until the command matches local
Codex help.

### Styled interactive terminal

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --theme crt-green
apex-infinite --path ~/projects/my-app/ --theme crt-amber
apex-infinite --path ~/projects/my-app/ --theme ibm-dos
```

Use this when the terminal supports color and normal Rich rendering. `auto`
selects `crt-green` in capable interactive terminals. Use an explicit
`--theme` when you want to opt back into styled output after an environment
constraint such as `NO_COLOR`.

### Plain, ASCII, and compact fallbacks

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --plain
apex-infinite --path ~/projects/my-app/ --plain --ascii
apex-infinite --path ~/projects/my-app/ --plain --ascii --compact
```

Use `--plain` for CI, logs, redirected output, remote shells, unreadable color
schemes, or `TERM=dumb`. Use `--ascii` when the terminal cannot render
non-ASCII glyphs reliably. Use `--compact` when the terminal height is limited
or you are collecting logs, but still expect errors, manager reasons, prompts,
DB writes, completion, timeouts, interrupts, and non-zero exits to remain
visible.

Environment behavior:

- `NO_COLOR` behaves like plain mode unless you pass an explicit `--theme`.
- `TERM=dumb`, non-TTY output, redirected output, and non-terminal Rich console
  paths default to plain output unless you force a theme.
- Non-UTF terminals should use `--ascii`, usually with `--plain`.
- Narrow terminals should use `--compact` and inspect history with
  `--history --verbose` only when needed.

### Event stream file

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --event-stream /tmp/apex-events.jsonl
```

Use this when another process should observe lifecycle facts while a human
operator still sees the normal CLI surface. The file is JSONL and is flushed
after every event.

### Machine-output JSONL

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --event-stream - --machine-output
```

Use this for wrappers or automation that read stdout. In this mode stdout is
reserved for JSONL events. Human rendering, terminal bell, and desktop
notifications are disabled.

Do not use `--event-stream -` without `--machine-output`; the CLI rejects that
combination so human output never mixes with JSONL on stdout. If a human should
watch the run while automation observes it, write events to a file path instead
of stdout.

### Optional visual wrapper source mode

```bash
cd apex-infinite-cli
python -m pip install -e ".[visual]"
apex-infinite-visual --dry-run --max-iterations 1
```

Use this only for the Linux visual wrapper source mode. The base CLI install
remains the default `pyproject.toml` dependency set; PySide6 and QML stay in
the optional `visual` extra.
Source/dev operation is the supported Hyperterminal preview path. Final
AppImage or binary publication remains gated on clean-machine launch evidence,
packaging inspection, license/module review, notices, checksum, dependency
inventory, and source/relink review.

Source-mode settings can be selected before launch:

```bash
cd apex-infinite-cli
apex-infinite-visual \
  --theme crt-amber \
  --effect-intensity 55 \
  --font-family "monospace" \
  --font-scale 1.05 \
  --plain-fallback
```

The wrapper supports green CRT, amber CRT, IBM DOS, and plain presets, plus
effect intensity, font family, font scale, reduced effects, and plain fallback.

For a headless smoke check:

```bash
cd apex-infinite-cli
QT_QPA_PLATFORM=offscreen apex-infinite-visual \
  --dry-run --max-iterations 1 --auto-close-ms 900
```

By default, wrapper dry-run uses fixture events so it does not require provider
API keys or live Codex execution. To launch the real CLI subprocess, pass
`--launch-cli`; the wrapper will build a guarded
`--event-stream - --machine-output` command and keep stderr separate for
failure display.

Fallback behavior:

- If PySide6 is missing, install `.[visual]`.
- If a display backend is unavailable, run the offscreen smoke command or use
  the base terminal CLI.
- If events are malformed, the wrapper shows an error state and keeps the log
  bounded instead of crashing.
- If the subprocess writes stderr or exits non-zero, the wrapper maps that to a
  visible error state.
- If the subprocess times out or the base CLI module cannot be launched, the
  wrapper maps that to `Timed out` or `CLI missing`.

### History inspection

```bash
cd apex-infinite-cli
apex-infinite --history
apex-infinite --history --path ~/projects/my-app
apex-infinite --history --verbose
```

Use this to inspect the last 50 logged records globally or for a single
project path. The scoped lookup expands `~`, verifies the directory exists, and
uses the same trailing-slash history key as normal run logging, so
`~/projects/my-app` and `~/projects/my-app/` find the same rows. Default
history is a compact ledger with timestamp, status, project key, command,
reason, and response summary. Add `--verbose` to expand reason, response, and
stored-state detail.

## What Happens Per Iteration

1. Load up to 15 prior records for the project from SQLite.
2. Summarize that history through the summarizer LLM prompt.
3. Choose the next action through the manager LLM prompt, unless `--start`
   overrides iteration 1.
4. Route the decision:
   - Known workflow command -> build a Codex skill invocation prompt
   - `help` -> emergency operator pause outside the normal workflow
   - `alldonebaby` -> stop and mark the run complete
   - Any other string -> send it to Codex as raw instructions
5. Execute `codex exec` with parsed `exec_flags` and the configured reasoning
   effort override, unless `--dry-run` is enabled.
6. Log the result into `history.db`.
7. Clear the CEO message after one iteration unless a new interruption occurs.

## Operator Controls

### Operator input

- `--ceo "..."` seeds the first iteration with explicit operator guidance.
- Normal manager routing should follow the latest command's `Next command:`
  line, not pause for input.
- If the manager outputs `help`, the CLI pauses and prompts for an operator
  response. Treat this as an emergency escape hatch, not standard workflow.
- If the manager does not need help, the CEO message is consumed once and then
  cleared.

### Interrupt handling

- Press `Ctrl+C` once to request a pause after the current step.
- At the next loop boundary the CLI prompts for CEO instructions or `quit`.
- Press `Ctrl+C` twice if you want to force exit immediately.

### Output depth

- Default mode prints a truncated agent response panel.
- `--verbose` prints a larger panel with up to 2000 characters of the full
  response.
- With `--history`, `--verbose` expands ledger details instead of adding a
  separate history-only flag.

## Recommended Operating Pattern

For a new project:

1. Run with `--dry-run` first.
2. Confirm the chosen provider, model, Codex binary, autonomy flags, and
   reasoning effort are correct.
3. Start with an explicit command such as `--start plansession`.
4. Add `--ceo` only for real constraints or priorities, not for routine noise.
5. Inspect history after major transitions with `--history --path ...`.

For an existing project:

1. Reuse the same absolute project path; trailing slash differences are okay,
   but symlinked or otherwise different absolute paths are separate history
   identities.
2. Review the recent history table before resuming.
3. Resume with `--start` only if you want to override manager autonomy.

## Signals To Watch

| Signal | Meaning | Action |
|--------|---------|--------|
| `Manager Decision:` | Current loop decision | Confirm it matches the project state |
| `*** MANAGER NEEDS CEO HELP ***` | Emergency pause outside normal workflow | Provide one concise external unblocker or restart with `--start` |
| `*** PROJECT COMPLETE! ***` | Manager emitted `alldonebaby` | Stop the run and review deliverables |
| `[TIMEOUT]` | `codex exec` exceeded the timeout | Narrow scope or inspect the underlying command |
| `[ERROR exit code N]` | Codex exited non-zero | Read stderr in the logged response |
| `LLM call failed after 3 attempts` | Provider call exhausted retries | Check API key, base URL, model, or connectivity |
| `event_stream_error` | Machine-readable event stream failure | Inspect the source event and retry with a writable path |
| `Output fallback: NO_COLOR` | Color was disabled by environment | Use plain output or pass an explicit `--theme` if color is intentional |
| `Output fallback: TERM=dumb` | Terminal reported a constrained mode | Use `--plain --ascii --compact` or a richer terminal |
| `Output fallback: non-terminal output` | Output is redirected or not attached to a terminal | Keep plain logs or pass an explicit `--theme` only for a capable destination |

## Safe Shutdown

- Preferred: respond `quit` when prompted after `help` or an operator interrupt.
- Acceptable: terminate the process if you do not need another history record.
- After exit, use `--history --path ...` to confirm the last recorded state.

## Local Data, Logs, And Retention

- **History**: `~/.apex-infinite/history.db` keeps raw workflow history
  indefinitely. Purge with `apex-infinite --purge-history` (add `--path`
  for one project, `--yes` for scripts). A one-time privacy notice covers
  this and provider-bound prompt traffic on the first human-mode run; its
  marker lives in `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/`.
- **Wrapper run logs**: real-CLI visual runs write the full JSONL event
  stream to `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/logs/`
  (`run-<utc>.jsonl`) by default. These are the export/diagnosis artifact
  for a run: structured, timestamped, secret-free registered events. Use
  `--reduced-logging` to disable, `--run-log-dir` to relocate, and delete
  files from the directory to purge. There is no automatic rotation;
  clean the directory as part of routine maintenance.
- **Production launcher logs**: `make production` writes separate preflight
  and live-run JSONL files to the same XDG state log directory unless
  `LOG_DIR` is set. Files are created with a private process umask, use unique
  UTC-plus-process identifiers, and require the same manual rotation policy.
- **Event export**: the visual event core can also export the currently
  filtered rows as JSON from the signal panel.
- **Provider traffic**: prompts can carry recent history, latest agent
  output, summaries, operator instructions, and project paths to the
  configured provider. Never place secrets or personal data in prompts or
  target-project output.

## Reference Archives

The `n8n-workflow/` directory is a historical reference archive for the
pre-CLI automation. It is not loaded by the Python package, the manager loop,
the visual wrapper, provider preflight, or tests. Archived workflow JSON may
contain old form defaults, local project examples, node credentials labels, and
operator prompts from the original n8n setup. Leave those values intact unless
you are intentionally curating the archive itself.

## Sample References

- [Plain dry-run transcript](transcripts/dry-run-plain.txt) shows a
  deterministic `--plain --ascii --compact --dry-run` run.
- [History ledger transcript](transcripts/history-ledger.txt) shows compact and
  verbose history display semantics.
- [Machine-output JSONL sample](transcripts/machine-output-events.jsonl) shows
  the stdout JSONL shape for wrappers and automation.
- [Visual wrapper productization](visual-wrapper-productization.md) records
  source-mode setup, settings, packaging gates, checksums, license notes, and
  clean-room verification.
- [Visual wrapper spike](visual-wrapper-spike.md) records the original wrapper
  decision, license notes, packaging risks, and backup path.

## Related Docs

- [History DB reference](history-db.md)
- [Event stream contract](event-stream.md)
- [Prompt contract](prompt-contract.md)
- [Troubleshooting guide](troubleshooting.md)
- [Visual wrapper productization](visual-wrapper-productization.md)
- [Visual wrapper spike](visual-wrapper-spike.md)
- [Visual wrapper boundary](visual-wrapper-boundary.md)
- [Transcript samples](transcripts/README_transcripts.md)
