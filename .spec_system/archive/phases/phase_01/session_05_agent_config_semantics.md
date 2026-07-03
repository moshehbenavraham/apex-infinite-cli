# Session 05: Agent Config Semantics

**Session ID**: `phase01-session05-agent-config-semantics`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Make Codex agent configuration parsing and documented reasoning-effort behavior match actual subprocess invocation behavior.

---

## Scope

### In Scope (MVP)

- Replace `exec_flags.split()` with shell-aware parsing via `shlex.split`, or migrate `exec_flags` to a validated YAML list.
- Add tests for quoted Codex options such as config overrides with spaces or quotes.
- Decide whether `model_reasoning_effort` should be translated into current Codex CLI config syntax.
- Implement reasoning-effort translation or remove the inert setting from config and docs.
- Update config validation and README examples to match the chosen behavior.
- Preserve Session 01 Codex invocation policy decisions.

### Out of Scope

- Replacing Codex CLI.
- Prompt contract changes unrelated to command construction.
- Full provider or model-selection redesign.

---

## Prerequisites

- [ ] Session 01 is complete so the supported default invocation policy is known.
- [ ] Current Codex CLI config syntax is verified from local help or official documentation.

---

## Deliverables

1. Robust exec flag tokenization or validated list-based config.
2. Clear, tested behavior for `model_reasoning_effort`.
3. Config and README text that no longer describe inert settings.

---

## Success Criteria

- [ ] Quoted exec flag values are passed to the Codex subprocess as intended.
- [ ] `model_reasoning_effort` either affects the generated Codex command or is absent from shipped config and docs.
- [ ] Config errors remain clear and actionable.
- [ ] Existing subprocess and prompt-routing tests remain green.
