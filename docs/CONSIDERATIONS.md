# Considerations

> Institutional memory for AI assistants. Updated between phases via carryforward.
> **Line budget**: 600 max | **Last updated**: Phase 01 (2026-07-03)

---

## Active Concerns

Items requiring attention in upcoming phases. Review before each session.

### Technical Debt
<!-- Max 5 items -->

- [P00] **CLI module pressure**: `src/apex_infinite/cli.py` still owns Click, config loading, LLM calls, SQLite, notifications, and workflow orchestration. Extract helpers only when the split lowers risk and has focused tests.
- [P00] **Prompt contract coupling**: Do not change `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or `build_codex_prompt()` unless prompt tests, README, and prompt-contract docs move in the same session.
- [P00] **History retention gap**: Local SQLite history keeps raw agent output, operator instructions, project paths, decisions, and timestamps without retention, purge, or redaction behavior.
- [P01] **Version identity mismatch**: Final smoke evidence found package metadata/build output and `apex-infinite --version` disagreeing. Align version sources before a public tagged release.
- [P00] **History compatibility**: Existing `~/.apex-infinite/history.db` files must remain readable without migration. Preserve the legacy `cc_response` column, normalized project path keys, and raw workflow facts.

### External Dependencies
<!-- Max 5 items -->

- [P00] **Provider and Codex prerequisites**: Provider API keys, local provider availability, and the configured Codex binary are runtime prerequisites. Never print, store, or emit API keys in history, events, docs, or tests.
- [P00] **Dependency governance**: Session 08 passed local `pip-audit`, but the CLI still lacks lockfiles or recurring CI/scheduled vulnerability scanning for base, dev, and wrapper requirements.
- [P01] **Codex CLI drift**: Supported Codex flags can change. Non-dry-run startup should keep using bounded help inspection and tests that reject stale configured flags before a loop begins.
- [P00] **Optional wrapper obligations**: PySide6/Qt Quick/QML belongs only in the optional Linux visual wrapper path, with LGPLv3/commercial obligations, generated-bundle review, notices, checksums, and source/relink materials before binary release.
- [P00] **Terminal-widget exclusions**: PyQt, qmltermwidget, QTermWidget, copied terminal-emulator code, and embedded pseudo-terminal behavior remain out of scope unless a later explicit decision changes the wrapper architecture.

### Performance / Security
<!-- Max 5 items -->

- [P00] **Raw durable facts only**: SQLite rows and JSONL events must contain operational facts only: no ANSI escapes, Rich markup, frame glyphs, visual tokens, secrets, copied-reference identifiers, or renderer snapshots.
- [P00] **Machine-output isolation**: Writing event JSONL to stdout is valid only with `--machine-output`; never mix JSONL with Rich or plain human output on stdout.
- [P00] **Provider transfer disclosure**: Recent history, latest agent output, summaries, and operator instructions can be sent to the configured LLM provider. Document this clearly before broader release.
- [P01] **Broad autonomy policy**: Phase 01 validates and documents effective Codex flags, but the default still uses a broad bypass flag. Future work should revisit opt-in or narrower permission policy.
- [P00] **Binary release gate**: The optional Linux wrapper is source-shippable only. Any AppImage/binary artifact needs artifact-specific license, notice, checksum, source/relink, and bundle review.

### Architecture
<!-- Max 5 items -->

- [P00] **Renderer boundary ownership**: Startup, iteration frames, manager decisions, prompt previews, execution results, DB notices, history, interrupts, and completion should continue through renderer helpers with injected `Console` support.
- [P00] **Event stream is the wrapper contract**: Visual surfaces must consume the importable emitter or line-buffered JSONL events, not scrape Rich/plain human output or parse terminal frames.
- [P00] **Wrapper as companion surface**: The Linux visual wrapper must launch or reuse the CLI workflow engine through the event boundary and must not fork manager decisions, prompt routing, storage, or safety behavior.
- [P00] **Clean-room visual translation**: Treat retro styling as conceptual requirements only. Do not copy code, QML, shaders, constants, assets, fonts, profiles, resource manifests, icons, build scripts, or terminal-emulator material.
- [P00] **Effect responsibility split**: Rich covers color, labels, layout, framing, status hierarchy, and low-fidelity separators. Glow, curvature, flicker, burn-in trails, RGB shift, and shader-like effects stay behind the optional wrapper boundary.

---

## Lessons Learned

Proven patterns and anti-patterns. Reference during implementation.

### What Worked
<!-- Max 15 items -->

- [P00] **Renderer-only snapshots**: Passing raw workflow facts to renderer snapshot objects enriched output while preserving prompt routing, subprocess behavior, SQLite rows, and tests.
- [P00] **Semantic labels over color**: Stable text labels such as `BOOT`, `ITERATION`, `DECISION`, `DRY RUN`, `LOGGED`, and `STOP` keep critical state visible in plain, ASCII, compact, `NO_COLOR`, and non-TTY modes.
- [P00] **Render-time history summaries**: History readability improved without schema migration by deriving labels, summaries, and truncation at display time only.
- [P00] **Event side channel**: JSONL lifecycle events stayed stable because they observe raw lifecycle facts instead of rendered terminal output.
- [P00] **Guarded machine stdout**: Requiring `--machine-output` for `--event-stream -` kept machine JSONL separate from human rendering and notification output.
- [P00] **Deterministic text fixtures**: ASCII transcripts and JSONL samples are easier to review, diff, and release-check than screenshots or ANSI captures.
- [P00] **Central clean-room boundary**: One visual-wrapper boundary document reduced drift across docs, tests, wrapper implementation, release checks, and license posture.
- [P00] **Optional wrapper lane**: Keeping PySide6/QML in `requirements-wrapper.txt` preserved headless/base CLI behavior while allowing source-mode wrapper productization.
- [P00] **Python-owned wrapper controls**: Validated Python settings, launcher behavior, and event adaptation made QML a display layer rather than a second workflow engine.
- [P00] **Release ledger mapping**: Mapping each PRD criterion to commands, inspections, focused fixes, or explicit gates made release verification auditable and concise.
- [P01] **Bounded startup probes**: `codex exec --help` validation catches stale flags without launching a mutating prompt; skip it for dry-run command inspection.
- [P01] **Shared command tokens**: Route startup validation, dry-run display, and subprocess launch through one token builder so docs, tests, and runtime cannot drift.
- [P01] **Event registry coverage**: Every lifecycle event emitted by startup code needs schema registration and file/stdout/machine-output regression coverage.
- [P01] **Explicit smoke environment**: Use repository `.venv/bin/python` and isolated `/tmp` smoke homes/artifacts so release evidence is reproducible across stale shells.
- [P01] **Parse smoke artifacts**: Validate JSONL event files and isolated history DB rows directly; do not rely on visual inspection of terminal output.

### What to Avoid
<!-- Max 10 items -->

- [P00] **Styled storage pollution**: Do not persist Rich markup, ANSI escapes, frame glyphs, truncation text, or display-only labels to SQLite or event payloads.
- [P00] **Scraping human output**: Wrappers and automation must not parse Rich frames, plain terminal text, or SQLite history when the JSONL/API event boundary exists.
- [P00] **Decorative opacity**: Do not let retro styling hide manager reasons, prompts, captured output, errors, completion state, or handoff information.
- [P00] **Graphical base install**: Do not make terminal CLI users install Qt, PySide6, PyQt, terminal widgets, image assets, shader assets, or display-server dependencies.
- [P00] **Raw stderr in product UI**: Product-facing wrapper failures should expose safe summaries and state labels, not raw subprocess stderr as UI text.
- [P00] **Binary release by implication**: Source-shippable wrapper status does not make AppImage/binary publication ready; complete artifact-specific legal and packaging gates first.
- [P00] **Prompt drift during UI work**: Do not edit manager routing text to support display-only concerns; use renderer/event metadata instead.
- [P01] **Whitespace flag parsing**: Do not split `codex.exec_flags` with plain whitespace; quoted Codex `-c` values need shell-aware tokenization or validated list config.
- [P01] **Inert documented config**: Do not document config fields unless dry-run output and command construction prove they affect the launched subprocess.
- [P01] **Ambient Python assumptions**: Do not rely on activated shell `python` for release smokes; stale virtualenvs can point at another project.

### Tool/Library Notes
<!-- Max 5 items -->

- [P00] **Rich**: Use injected consoles and width-specific records for tests; keep plain and ASCII renderers free of box-drawing glyphs and live-only output.
- [P00] **Click**: Use `CliRunner` coverage for new flags, invalid theme values, config precedence, and incompatible event-output combinations.
- [P00] **SQLite**: Use temporary DB paths or monkeypatched `DB_DIR`/`DB_PATH` in tests; cover empty, sparse legacy, short, and long history rows.
- [P00] **JSONL events**: Serialize with ASCII-safe JSON, validate payload types and unsafe strings, flush line-by-line, and keep event names importable for tests.
- [P00] **PySide6/QML**: Keep imports wrapper-only, run offscreen smoke and QML lint, and validate settings in Python before values reach QML.

---

## Resolved

Recently closed items (buffer - rotates out after 2 phases).

| Phase | Item | Resolution |
|-------|------|------------|
| P00 | UI config gap | Added validated UI settings, built-in/custom themes, CLI overrides, and environment-aware fallback behavior. |
| P00 | Subprocess visibility gap | Added renderer-facing process state, timeout cleanup coverage, compact history, and preserved stdout/stderr semantics. |
| P00 | Event stream gap | Added importable emitter API and guarded JSONL streams for wrapper and automation consumers. |
| P00 | Wrapper productization uncertainty | Completed PySide6/QML spike and source-mode productization while keeping binary distribution gated. |
| P01 | Codex invocation compatibility | Replaced stale default flags, added bounded startup validation, and verified real nested Codex smoke. |
| P01 | Provider preflight event contract | Registered provider lifecycle event names and covered file/stdout/machine-output success and failure paths. |
| P01 | History path lookup drift | Shared normalized project path keys across writes and scoped reads without a schema migration. |
| P01 | Output observability polish | Replaced internal plain labels with `STATUS` and emitted bounded safe response previews. |
| P01 | Agent config semantics | Added shell-aware flag parsing, fail-fast option validation, and active reasoning-effort command output. |
| P01 | Smoke environment ambiguity | Documented repository virtualenv smoke commands and reran quality, provider, event, wrapper, and real Codex gates. |

---

*Auto-generated by carryforward. Direct edits allowed but may be overwritten.*
