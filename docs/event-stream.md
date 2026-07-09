# Apex Infinite CLI Event Stream

## Purpose

The event stream is the machine-readable lifecycle boundary for wrappers,
tests, and automation. It reports raw operational facts as JSONL without
requiring consumers to parse Rich panels, plain text, history rows, or terminal
frames.

Normal human output remains the default. File event streams are a side channel.
Stdout JSONL is available only in explicit machine-output mode.

## CLI Modes

Write events to a file while keeping normal human output:

```bash
apex-infinite --path ~/projects/my-app/ --event-stream /tmp/apex-events.jsonl
```

Reserve stdout for JSONL and suppress human rendering, terminal bell, and
desktop notifications:

```bash
apex-infinite --path ~/projects/my-app/ --event-stream - --machine-output
```

Guardrails:

- `--event-stream -` requires `--machine-output`.
- `--machine-output` requires `--event-stream`.
- `--event-stream PATH` without `--machine-output` leaves normal human stdout
  unchanged and writes JSONL to `PATH`.
- Wrappers that need human-readable logs should use a file event stream and
  leave stdout/stderr for the normal terminal surface.
- Wrappers that need machine-readable stdout should use
  `--event-stream - --machine-output` and treat stdout as JSONL only.

## Event Shape

Each line is one JSON object:

```json
{"event":"startup_begin","payload":{"dry_run":true,"event_stream":true,"machine_output":false,"max_iterations":1},"timestamp":"2026-07-03T00:00:00Z","version":1}
```

Fields:

| Field | Type | Meaning |
|-------|------|---------|
| `version` | integer | Event schema version. Current value is `1`. |
| `event` | string | Stable snake_case event name. |
| `timestamp` | string | UTC timestamp in `YYYY-MM-DDTHH:MM:SSZ` format. |
| `payload` | object | Raw JSON-safe event facts. |

Payload values are strings, numbers, booleans, null, arrays, and objects only.
The emitter rejects non-JSON objects, non-finite floats, ANSI escapes, Rich
markup, frame glyphs, display token names, secret-looking keys, and
secret-looking values.

## Event Names

These names are emitted by the current CLI flow:

Startup and configuration:

- `startup_begin`
- `config_loaded`
- `ui_resolved`
- `project_resolved`
- `codex_flags_check_started`
- `codex_flags_check_failed`
- `codex_flags_check_finished`
- `provider_check_started`
- `provider_check_failed`
- `provider_check_finished`
- `startup`

Hyperterminal design-lane facts (emitted after `project_resolved`):

- `spec_system_detected` - `.spec_system/` detection facts for the resolved
  project: `detected`, plus `has_prd`, `phase_count`, and `latest_phase`
  when detected.
- `autonomy_policy_resolved` - `dry_run`, `max_iterations`,
  `start_command`, `risk_level`, and `provider_preflight` before the loop
  starts.

Provider preflight events are startup lifecycle events. Normal startup emits
them after project resolution, after Codex flag validation when that non-dry-run
validation runs, and before the main loop `startup` event. `--check-provider
--event-stream PATH` emits the same provider lifecycle names and exits before
project selection or loop startup. Failure paths emit `provider_check_failed`
followed by the generic `error` event.

Loop lifecycle:

- `iteration_started`
- `history_fetched`
- `history_summarize_started`
- `history_summarize_finished`
- `manager_decision_started`
- `manager_decision_finished`
- `prompt_built`
- `prompt_dispatched`

Codex subprocess:

- `codex_dry_run`
- `codex_started`
- `codex_finished`
- `codex_error`
- `codex_timeout`
- `response_summarized`

Storage, operator, and stop states:

- `db_log_started`
- `db_log_finished`
- `help_requested`
- `operator_interrupt_requested`
- `operator_interrupt_quit`
- `operator_input_received`
- `workflow_completed`
- `max_iterations_reached`
- `run_stopped`
- `event_stream_error`

Registered names reserved for the visual wrapper and future CLI sessions
(payloads must follow the same validation rules; the wrapper may ingest
them synthetically):

- `spec_session_resolved` - current spec session identity (`session`).
- `task_progress` - session task checklist progress (`done`, `total`).
- `artifact_detected` - a safe artifact reference (`name` or `path`).
- `run_duration_tick` - elapsed run seconds (`seconds`).
- `wrapper_capabilities_resolved` - render backend facts from
  `render_caps.capabilities_payload()`.
- `doctor_started`, `doctor_check`, `doctor_finished` - launch-readiness
  diagnostics with display-safe `status` values `pass`, `warn`, `fail`.
- `codex_flags_resolved` - resolved Codex flag compatibility facts.

The registry also accepts compatibility names for wrapper experiments and
future migrations: `config_resolved`, `history_summary_started`,
`history_summary_completed`, `manager_decision_completed`, `codex_completed`,
`codex_failed`, `output_summary`, `db_logged`, `completion`, and `error`.
Current code may emit `error` for startup, history-summary, or manager-decision
failures. Consumers should ignore unknown future event names only after logging
the raw event for diagnosis.

## Event Extension Rules

The visual wrapper must not scrape missing workflow facts from Rich panels,
plain terminal output, SQLite history display rows, ANSI captures, or
terminal-control sequences. If a visual surface needs a new fact, add a stable
registered event or an explicit wrapper control.

For every new event:

- Add the name to `src/apex_infinite/events.py`.
- Cover file-stream behavior in tests.
- Cover `--event-stream - --machine-output` behavior in tests.
- Keep payloads JSON-safe, bounded, and factual.
- Exclude secrets, ANSI escapes, Rich markup, frame glyphs, renderer
  snapshots, copied reference identifiers, visual token values, and full
  prompts or subprocess output.
- Prefer primitive payload fields and small objects over display-ready strings.

## Payload Principles

Events report bounded facts, not full terminal output:

- Project path key, provider name, model name, dry-run state, and iteration
  number when relevant.
- Provider preflight lifecycle facts such as provider name, model name, base
  URL, completion-check state, model count, and controlled failure message.
- Prompt lengths and bounded response summaries instead of full prompts or full
  Codex output.
- Return code, elapsed seconds, timeout seconds, and output lengths for
  subprocess facts.
- DB log start/finish state around existing `db_log()` calls.
- Operator input action and input length, not the input text.

Events do not include:

- Provider API keys or full provider config maps.
- Rich renderables, ANSI escapes, frame glyphs, display labels, or renderer
  snapshots.
- Theme token values such as foreground, border, panel, or separator styles.
- Copied visual reference data, shaders, images, fonts, profile data, or
  terminal-emulator implementation details.

## Response Summary Preview Contract

`response_summarized` payloads include:

| Field | Type | Meaning |
|-------|------|---------|
| `source` | string | Response source, such as `codex_dry_run`, `codex`, `codex_timeout`, `codex_missing`, or `codex_error`. |
| `length` | integer | Full raw response length in characters. |
| `line_count` | integer | Full raw response line count. |
| `has_output` | boolean | Whether the raw response contains non-whitespace text. |
| `preview` | string | Whitespace-normalized response preview, bounded to the CLI response preview limit. |
| `preview_suppressed` | boolean | `true` when the preview candidate was withheld for payload safety. |

Safe short output, such as dry-run commands or
`APEX_INFINITE_SUBPROCESS_SMOKE_OK`, appears directly in `preview`.

Long output is truncated deterministically with `...`. If the preview candidate
contains ANSI escapes, Rich markup, frame glyphs, display-theme tokens, or
secret-like values, the event still writes successfully with `preview: ""` and
`preview_suppressed: true`. Expected unsafe previews do not produce
`event_stream_error` rows.

Response previews are event-stream metadata only. They are not written to
SQLite history rows and do not change the raw Codex response stored by the
existing history contract.

## Example File Stream

```jsonl
{"event":"startup_begin","payload":{"dry_run":true,"event_stream":true,"machine_output":false,"max_iterations":1},"timestamp":"2026-07-03T00:00:00Z","version":1}
{"event":"config_loaded","payload":{"config_path":"config.yaml","model_name":"qwen2.5-coder:7b-instruct-q4_K_M","provider_name":"ollama"},"timestamp":"2026-07-03T00:00:01Z","version":1}
{"event":"ui_resolved","payload":{"ascii_only":false,"color_enabled":false,"compact":false,"constraint_reason":"non-terminal output","effect_level":"off","plain":true,"requested_theme":"auto","theme_name":"plain"},"timestamp":"2026-07-03T00:00:01Z","version":1}
{"event":"project_resolved","payload":{"project_path":"/home/user/projects/my-app/"},"timestamp":"2026-07-03T00:00:01Z","version":1}
{"event":"provider_check_started","payload":{"base_url":"http://localhost:11434/v1","completion_check":false,"model_name":"qwen2.5-coder:7b-instruct-q4_K_M","provider_name":"ollama"},"timestamp":"2026-07-03T00:00:01Z","version":1}
{"event":"provider_check_finished","payload":{"base_url":"http://localhost:11434/v1","completion_checked":false,"model_count":1,"model_name":"qwen2.5-coder:7b-instruct-q4_K_M","provider_name":"ollama"},"timestamp":"2026-07-03T00:00:01Z","version":1}
{"event":"startup","payload":{"ceo_present":false,"config_path":"config.yaml","dry_run":true,"event_stream_path":"/tmp/apex-events.jsonl","machine_output":false,"max_iterations":1,"model_name":"qwen2.5-coder:7b-instruct-q4_K_M","project_path":"/home/user/projects/my-app/","provider_name":"ollama","start_command":"implement","theme_name":"plain"},"timestamp":"2026-07-03T00:00:01Z","version":1}
```

See
[machine-output-events.jsonl](transcripts/machine-output-events.jsonl)
for a deterministic stdout JSONL sample that covers startup, UI resolution,
prompt dispatch, dry-run execution, DB logging, and stop events.

## Failure Behavior

If an event payload or write fails in normal human-output mode, the CLI prints
a visible `Event Stream` error through the renderer and keeps the workflow
decision path unchanged.

If a failure occurs in machine-output mode, the CLI tries to emit an
`event_stream_error` event with the failed source event and error type. If the
stream itself is no longer writable, no human fallback is printed to stdout.

## Wrapper Guidance

Wrappers should consume the JSONL stream or import `apex_infinite.events`
directly. They should not parse terminal output, Rich markup, history display
rows, or frame-like text. The event stream is append-only during a run and is
flushed after every event so wrapper state can update incrementally.

The event stream is the supported visual-wrapper state boundary. A wrapper may
show its own log viewport or styled panels, but those views must be derived
from events or an importable API, not from scraping Rich panels, plain output,
ANSI captures, or SQLite history display text.

Related docs:

- [Operator runbook](operator-runbook.md)
- [Prompt contract](prompt-contract.md)
- [Troubleshooting guide](troubleshooting.md)
- [Visual wrapper boundary](visual-wrapper-boundary.md)
- [Transcript samples](transcripts/README_transcripts.md)
