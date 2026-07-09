# Incident Response

## Scope

Apex Infinite CLI is a local developer tool, not a hosted production service.
Incidents are local runtime, provider, data-handling, release, or wrapper
failures during operator use or release smoke checks.

## Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 | Real run modified the wrong project or exposed secrets. | Immediate stop and containment. |
| P1 | Real workflow cannot start or release smoke fails. | Same working session. |
| P2 | Non-critical docs, display, wrapper, or local-provider issue. | Next focused fix session. |

## First Response

1. Stop the current run. Press Ctrl+C once to request a pause, or twice only
   when the current process must be terminated.
2. Preserve evidence outside the repository when possible: terminal output,
   event stream, `/tmp` smoke path, command line, provider name, model, and git
   status.
3. Do not copy provider keys, full config maps, local history databases, or
   customer data into an issue or report.
4. Check `docs/troubleshooting.md` for the matching symptom.
5. Record the exact verification command that reproduces or clears the issue.

## Common Incidents

### Provider Preflight Fails

**Symptoms**: `Provider preflight failed`, unavailable configured model, or
`--check-provider` exits non-zero.

**Resolution**:

1. Check `.env`, `src/apex_infinite/config.yaml`, and any `--provider` or
   `--model` override.
2. For local Ollama, run `./scripts/check-ollama.sh --chat`.
3. For hosted providers, verify network access and provider status without
   printing API keys.

### Codex Flags Rejected Before Startup

**Symptoms**: `Malformed codex.exec_flags` or configured flags are not
supported by local `codex exec --help`.

**Resolution**:

1. Run `codex exec --help`.
2. Fix quoting or stale flags in the active config.
3. Run `.venv/bin/apex-infinite --path <project> --dry-run` to inspect the
   effective command before real execution.

### Event Stream Cannot Be Written

**Symptoms**: `Event stream error`, missing JSONL rows, or mixed human output
in stdout JSONL.

**Resolution**:

1. Use a writable file path for `--event-stream`.
2. Use `--event-stream - --machine-output` when stdout must be JSONL only.
3. Validate the JSONL file before using it as wrapper or release evidence.

### Local History Contains Sensitive Data

**Symptoms**: Operator instructions, agent responses, or project paths include
information that should not remain in local history.

**Resolution**:

1. Stop the run.
2. Protect or remove `~/.apex-infinite/history.db` manually.
3. Avoid placing secrets or personal data in future operator instructions or
   target-project outputs.

### Visual Wrapper Fails To Start

**Symptoms**: missing PySide6, wrapper `CLI missing`, offscreen smoke failure,
or wrapper timeout.

**Resolution**:

1. Install the visual extra: `.venv/bin/python -m pip install -e ".[visual]"`.
2. Run the base CLI command directly.
3. Run the offscreen smoke command from the operator runbook.
4. Treat binary packaging as gated until license, notices, checksums, and
   source/relink review are complete.

## Related Docs

- [Troubleshooting guide](../troubleshooting.md)
- [Operator runbook](../operator-runbook.md)
- [Event stream contract](../event-stream.md)
- [Security posture](../../.spec_system/SECURITY-COMPLIANCE.md)
