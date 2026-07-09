# Security & Compliance

> Cumulative security posture and GDPR compliance record. Updated between phases via carryforward.
> **Line budget**: 1000 max | **Last updated**: Phase 01 (2026-07-03)

---

## Current Security Posture

### Overall: ACCEPTABLE WITH DOCUMENTED RISK

The 2026-07-09 productization pass closed the four open findings: local
history now has a purge path and a first-run privacy notice, the broad Codex
bypass default is a documented accepted risk with mandatory autonomy summary
and dry-run-first onboarding (ADR 0001 #8), provider-bound prompt traffic is
disclosed in README and the first-run notice, and a recurring CI `pip-audit`
lane scans base, dev, and visual dependencies weekly and on dependency
changes.

| Metric | Value |
|--------|-------|
| Open Findings | 0 |
| Critical/High | 0 |
| Medium/Low | 0 |
| Phases Audited | 2 |
| Last Clean Phase | P01 (2026-07-09 update) |

---

## Open Findings

Active security or GDPR issues requiring attention. Ordered by severity.

### Critical / High

No open critical or high findings.

### Medium / Low

No open medium or low findings.

---

## GDPR Compliance Status

### Overall: LOCAL TOOL / DISCLOSED

The project is not an end-user data service, but it can process operator text,
target-project paths, agent responses, and provider-bound prompts. Treat local
history and provider requests as potentially sensitive operational data. As of
2026-07-09 the tool shows a one-time first-run privacy notice, ships a CLI
purge path (`--purge-history`, optionally scoped with `--path`), and documents
provider-bound prompt transfer in README and the notice. Raw history rows are
retained until purged; redaction of individual fields remains out of scope for
a local operator tool and is covered by the purge path.

### Personal Data Inventory

| Data Element | Source | Storage | Purpose | Legal Basis | Retention | Deletion Path | Since |
|--------------|--------|---------|---------|-------------|-----------|---------------|-------|
| Project path | CLI `--path` and current project | Local SQLite history | Scope workflow history and resume context | Operator-initiated local processing | Indefinite | Manual DB deletion only | P00 |
| Operator instructions | CLI input and CEO/start options | Local SQLite history and LLM prompts | Guide workflow decisions | Operator-initiated local processing | Indefinite locally; provider policy externally | Manual DB deletion only | P00 |
| Agent responses | Codex subprocess output | Local SQLite history and LLM prompts | Resume and route workflow state | Operator-initiated local processing | Indefinite locally; provider policy externally | Manual DB deletion only | P00 |
| Manager decisions and reasons | Manager LLM response | Local SQLite history | Audit and resume workflow state | Operator-initiated local processing | Indefinite | Manual DB deletion only | P00 |
| Provider API keys | Environment or `.env` | Process environment; provider client | Authenticate provider calls | Operator configuration | Until operator rotates/removes | Remove env or `.env` entry | P00 |
| Desktop notification text | CLI runtime state | Local OS notification surface | Alert operator on pause or completion | Operator-initiated local processing | OS dependent | OS notification cleanup | P00 |

### Compliance Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| Data collection has documented purpose | PASS | History exists to resume and summarize workflow state. |
| Consent obtained before data storage | PASS | One-time first-run privacy notice shown before history storage and provider traffic (2026-07-09). |
| Data minimization verified | PARTIAL | Recent rows are summarized; raw history is retained until the operator purges it. |
| Deletion/erasure path exists | PASS | `apex-infinite --purge-history` deletes all or per-project rows (2026-07-09). |
| No PII in application logs | PARTIAL | No intentional PII collection; event payloads reject secret-like values, but raw prompts/outputs in history are unscrubbed by design. |
| Third-party transfers documented | PASS | README Data section and the first-run notice document provider-bound prompt traffic; provider-specific legal posture is the operator's provider choice. |

---

## Dependency Security

### Current Vulnerabilities

No known vulnerable dependencies from the Phase 01 local audit.

| Package | Version | Severity | CVE | Status |
|---------|---------|----------|-----|--------|
| - | - | - | - | No known vulnerabilities from local `pip-audit` evidence on 2026-07-03. |

Notes:

- Base runtime dependencies remain terminal-only: Click, OpenAI Python SDK, python-dotenv, Rich, PyYAML, and Python standard library SQLite/subprocess modules.
- Development dependencies include pytest, pytest-cov, pytest-mock, black, pylint, and pip-audit.
- Optional wrapper dependencies remain isolated in the `visual` extra and include PySide6 and Nuitka.
- Recurring dependency audit automation and dependency locking remain open under [P00-S04].
- Phase 01 package build and audit passed locally; `apex-infinite-cli` was skipped by `pip-audit` because it is not on PyPI.

---

## License Compliance

| Area | Status | Notes |
|------|--------|-------|
| Base CLI dependencies | PASS | Runtime dependency set is terminal-only and does not include graphical wrapper dependencies. |
| Visual inspiration boundary | PASS | Phase 00 scans found no tracked reference implementation material or assets in source/docs. |
| Optional wrapper source mode | PASS | PySide6/QML remains optional in the `visual` extra; source mode is separate from the base CLI. |
| Binary/AppImage distribution | GATED | No binary artifact is published. Future binary release must complete generated-bundle review, license/module review, notices, SHA256 checksums, and source/relink instructions. |
| Excluded components | REQUIRED | Do not add PyQt, terminal-widget libraries, copied terminal-emulator code, copied shader code, copied images, copied icons, copied fonts, copied resource manifests, or copied profile data unless scope changes explicitly. |

---

## Resolved Findings

Recently closed items. Compressed after 2 phases.

| ID | Finding | Severity | Resolved | Phase | Resolution |
|----|---------|----------|----------|-------|------------|
| P00-S01 | Local history has no retention or redaction controls | Medium | 2026-07-09 | P01 | Added `--purge-history` (all or per-project, confirmation-gated) plus a first-run privacy notice; retention documented in README. |
| P00-S02 | Autonomous execution flags need explicit operator safety policy | Medium | 2026-07-09 | P01 | Accepted-risk release policy recorded in ADR 0001 #8 with mandatory autonomy summary, dry-run-first onboarding, and setup-time warning. |
| P00-S03 | Provider-bound data transfer disclosure is incomplete | Medium | 2026-07-09 | P01 | README Data section and the first-run privacy notice document provider-bound prompt traffic and secret/PII warnings. |
| P00-S04 | Dependency audit is local-only | Low | 2026-07-09 | P01 | Added `.github/workflows/security-scan.yml`: weekly scheduled and dependency-change-triggered `pip-audit` across base, dev, and visual lanes. |
| P00-S05 | Event-stream payload safety and stdout isolation | Medium | 2026-07-03 | P00 | Guarded `--event-stream -` with `--machine-output`; release smokes verified JSONL schema and unsafe-token exclusion. |
| P00-S06 | Visual-wrapper clean-room uncertainty | Medium | 2026-07-03 | P00 | Clean-room scans found no copied reference source/assets; binary publication remains gated for artifact-specific review. |

---

## Phase History

| Phase | Sessions | Security | GDPR | Findings Opened | Findings Closed |
|-------|----------|----------|------|-----------------|-----------------|
| P01 | 6 | AT RISK | NON-COMPLIANT / LOCAL TOOL | 0 | 0 |
| P00 | 8 | AT RISK | NON-COMPLIANT / LOCAL TOOL | 6 | 2 |

---

## Recommendations

1. Keep the base CLI free of graphical dependencies and preserve the clean-room boundary for future visual-wrapper artifacts.
2. Review the weekly `pip-audit` CI results and act on new advisories promptly; consider a lockfile if reproducibility requirements grow.
3. Revisit field-level history redaction if the tool is ever distributed beyond single-operator local use.

---

*Auto-generated by carryforward. Direct edits allowed but may be overwritten.*
