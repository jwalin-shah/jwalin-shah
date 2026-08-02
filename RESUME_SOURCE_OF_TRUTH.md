# Jwalin Shah — Resume Source of Truth

Last audited: 2026-08-02

This is the durable working file behind the one-page résumé. It records what belongs in the master version, what is supported by public or private evidence, what should be tailored for a role, and what still needs proof before it is used.

## Master positioning

**Target identity:** AI Systems Engineer — Agent Reliability, Evaluation & Local Inference

**Core line:** Builds systems that constrain, observe, and verify probabilistic agents under real-world constraints.

**Why this is the strongest overall story:** The portfolio is not a collection of unrelated AI demos. Its repeated pattern is designing deterministic systems around nondeterministic models: retrieval with explicit abstention, isolated agent execution, fresh-checkout verification, local inference, benchmark harnesses, trace analysis, formal methods, and operational reliability on physical robots.

The master résumé should optimize for AI systems, agent infrastructure, evaluation, reliability, retrieval, and applied research roles. Robotics is credible supporting evidence, but it should not become the headline unless a role is specifically physical-AI focused.

## One-page master structure

1. **Experience:** OpenHuman → Break the Web / LiveLM → Skild AI
2. **Selected systems:** Bridge → OfficeQA Arena → Voice Engine
3. **Skills:** systems and evaluation capabilities first; tools second
4. **Education and leadership:** one compact block

*(Jarvis is variant-only — see master decision below.)*

**Master decision (2026-08-02):** Jarvis is off the one-page master. Exact gates remain for a local-agent / Apple variant; on the master page they duplicate OpenHuman and the archived repo reads stale next to Bridge / OfficeQA / Voice.

## Claim ledger

Status legend:

- **PUBLIC:** directly supported by a public repository, upstream pull request, or public project artifact.
- **PRIVATE:** supported by a private repository or internal artifact available during this audit; safe when accurate, but not independently visible to a recruiter.
- **USER:** established by the candidate; preserve a private proof packet where possible.
- **NEEDS PROOF:** plausible or previously used, but the backing artifact was not located.
- **EXCLUDE:** misleading, obsolete, attributable to a fork, or contradicted by current project status.

| ID | Canonical claim | Status | Evidence / audit note | Résumé treatment |
|---|---|---|---|---|
| OH-01 | 69 merged upstream OpenHuman PRs | PUBLIC | 100 recent authored PRs were reviewed; 69 were merged. Representative work: [#1259](https://github.com/tinyhumansai/openhuman/pull/1259), [#803](https://github.com/tinyhumansai/openhuman/pull/803), [#760](https://github.com/tinyhumansai/openhuman/pull/760), [#855](https://github.com/tinyhumansai/openhuman/pull/855), [#1469](https://github.com/tinyhumansai/openhuman/pull/1469). | Use exactly “69 merged upstream PRs.” Do not substitute branch commit totals. |
| OH-02 | SQLite-backed contact resolution/scoring with CNContactStore | PUBLIC | Merged in [OpenHuman #1259](https://github.com/tinyhumansai/openhuman/pull/1259), including a mockable cross-platform source. | Use. |
| OH-03 | Refactored ~1,500 lines of CLI adapters into domain modules | PUBLIC | Merged in [OpenHuman #758](https://github.com/tinyhumansai/openhuman/pull/758). | Use. |
| OH-04 | Added 196 tests across MCP, services, utilities, and autocomplete | PUBLIC | Merged in [OpenHuman #855](https://github.com/tinyhumansai/openhuman/pull/855). | Use. |
| OH-05 | “Owned and shipped life_capture / curated_memory A1–A7” | EXCLUDE | The architecture and sequenced branches were real, but most A1–A7 PRs were closed without merge. The people/contact slice later landed separately. | Say “designed/prototyped” only when relevant; never say all A1–A7 shipped. |
| BTW-01 | LiveLM retrieval over ~80K indexed canonical facts at ~11 ms warm p50 | PRIVATE | `btw-v1` system report records 84,841 canonical facts, 79,956 indexed, and 11 ms p50. | Use in experience; prepare a sanitized public case study if possible. |
| BTW-02 | 71-question benchmark across three serving paths plus 512 probes | PRIVATE | `btw-v1/evals/README.md` documents 71 hand-labeled questions × three paths and a 512-query probe set. | Use. |
| BTW-03 | Eight independently measured MCP stages | NEEDS PROOF | The exact eight-stage definition was not found in the audited evaluation documentation. | Omit until a named stage map and results artifact exist. |
| SK-01 | Built systems across five robotic platforms | USER | Consistent across prior résumé materials and candidate history. | Use; preserve platform list privately. |
| SK-02 | ~50% operational-overhead reduction and ~40% task-success improvement | USER | Candidate-established internal metrics; no public source expected. | Use approximate symbols and retain calculation notes, before/after dates, and sample sizes privately. |
| SK-03 | 25+ live demos with zero failures during $1B Series C | USER | Candidate-established operational record. | Use; retain demo log or manager corroboration privately. |
| SK-04 | Hired/scaled 30+ operators | USER | Candidate-established leadership record. | Use “scaled a 30+ operator program” in the master; use “hired” only when the role values recruiting ownership. |
| BR-01 | Bridge isolates agent execution with worktrees, sandboxing, and fresh-checkout verification | PRIVATE | Current `bridge` repository documentation and implementation. | Use; strongest flagship systems project. |
| BR-02 | 77 invariants cataloged; 52 checked/proved; 28 PBT checkers; 8 Z3 proofs; 5 TLA+ models; Lean proofs | PRIVATE | Current `bridge/AGENTS.md` and proof directories; largest model explores ~1.58M states. | Use exact numbers while they remain current. |
| BR-03 | “Fixed one fail-open gate, hardened six adapters, cataloged nine failure modes” | NEEDS PROOF | Older framing is weaker and the exact historical denominator is not as cleanly represented as the current invariant/proof corpus. | Replace with BR-01/BR-02. |
| OA-01 | 184.5/246 (75%) on 246 tasks for $1.71 | PUBLIC | [officeqa-arena](https://github.com/jwalin-shah/officeqa-arena) README and run artifacts. | Use exact score, denominator, pass rate, and cost. |
| OA-02 | 12 architecture rounds and ~4,400 evaluations | PUBLIC | Project README and evaluation history. | Use when space permits. |
| OA-03 | Evidence selection caused 48% of failures; correctly grounded Python answers had 0% arithmetic errors | PUBLIC | Published trace-analysis findings in the project. | Use; this is more distinctive than “multi-agent.” |
| VO-01 | Fully local Swift/CoreML dictation pipeline | PUBLIC | [voice-engine-swift](https://github.com/jwalin-shah/voice-engine-swift) code and architecture map. | Use. |
| VO-02 | 348/349 tests pass; one known CoreML OS-runtime failure | PUBLIC | Current project map/status. | Use with the failure stated honestly. |
| VO-03 | 560-clip external benchmark and specific WER improvements | NEEDS PROOF | Previously established in résumé work, but the public benchmark output was not found in the current repository audit. | Omit numbers until the benchmark report and reproduction command are committed. |
| JA-01 | 0.42 s mean / 1.15 s p95, Hit@5 0.88, 96.2% hallucination-gate pass | PUBLIC | [jarvis-ai-assistant](https://github.com/jwalin-shah/jarvis-ai-assistant) README and evaluation artifacts. | Best swap-in for local-agent roles. |
| HB-01 | HomeBase has Lean, Dafny, TLA+, and restart-verification artifacts | PUBLIC | [homebase](https://github.com/jwalin-shah/homebase) contains real proof and fixture artifacts. | Do not use in master yet because root docs still describe the system as design/not implemented. |
| AX-01 | Axioms is a reusable invariant corpus | PUBLIC | [axioms](https://github.com/jwalin-shah/axioms) is active, but README counts conflict with newer commits. | Supporting portfolio item only until counts and release story are reconciled. |
| FM-01 | Firstmate platform infrastructure | EXCLUDE | Repository history states the fork infrastructure is not original work. | Never claim platform authorship; claim only clearly original downstream work. |
| TL-01 | Tensor Logic implementation | EXCLUDE | Current README says pre-implementation. | Keep off résumé until a working evaluated system exists. |
| RR-01 | RoboReplan as a current flagship | EXCLUDE | Current README marks it deprecated/superseded. | Mention only as historical work for a tightly matched robotics role. |

## GitHub portfolio decision

The audit reviewed all 122 repositories owned by `jwalin-shah` at the metadata level, then deep-inspected the projects most likely to improve the résumé and upstream OpenHuman contribution history.

### Tier 1 — master résumé

| Project | Why it earns space | Current risk |
|---|---|---|
| [OpenHuman contributions](https://github.com/tinyhumansai/openhuman) | High-volume merged upstream work across Rust, TypeScript, memory, RPC, privacy, security, and reliability | Keep merged work distinct from closed personal-index branches |
| `bridge` | Most differentiated proof that the reliability thesis is implemented, not just stated | Private and recruiter-facing README is stale; needs a sanitized public case study |
| [officeqa-arena](https://github.com/jwalin-shah/officeqa-arena) | Excellent benchmark discipline, exact cost/quality result, and a non-obvious failure-analysis conclusion | Archived status is acceptable if framed as completed research |
| [voice-engine-swift](https://github.com/jwalin-shah/voice-engine-swift) | Native, local, constrained inference with a large test surface | Public numeric WER report is missing; one OS-level regression remains |
| [Jarvis](https://github.com/jwalin-shah/jarvis-ai-assistant) | Exact latency, retrieval, throughput, and hallucination-gate evidence; clear precursor to OpenHuman | Older and archived, so it is the first master project to cut when tailoring |
| `btw-v1` / LiveLM | Strong real-time grounding and explicit abstention architecture | Private evidence; publish a sanitized evaluation report |
| Skild AI systems | Real-world operational reliability and robotics constraints | Metrics need a private proof packet because they cannot be public |

### Tier 2 — role-specific swaps

| Project | Use when | Why it is not in the one-page master |
|---|---|---|
| [Inbox](https://github.com/jwalin-shah/inbox) | Personal data, ambient interfaces, productivity agents | Broad integration story but less measured than the Tier 1 set |
| [HomeBase](https://github.com/jwalin-shah/homebase) | Agent control planes/formal methods after docs are repaired | Repository status language contradicts implemented artifacts |
| [Axioms](https://github.com/jwalin-shah/axioms) | Safety case, assurance, formal methods | Needs a stable release, consistent counts, and adoption story |
| `data-connect-framework` | Data connectors and ingestion infrastructure | Less differentiated than OpenHuman/LiveLM |
| GemmaBot / AGI House work | Robotics-specific roles | Useful physical-AI evidence, but the master already has stronger systems proof |

### Tier 3 — archive or omit

Fork-heavy repositories, pre-implementation concepts, deprecated experiments, coursework, templates, and tiny one-off utilities should remain on GitHub but should not consume résumé space. The résumé is strongest when it shows a small number of systems with measured reliability, not the total number of projects.

## What to build or repair next

Ordered by likely résumé return on effort:

1. **Publish a Bridge case study.** Create a sanitized public repository or technical write-up with the threat model, spawn/verify/deliver architecture, one real failure trace, the invariant matrix, proof commands, and a fresh-checkout demo. This is the single highest-leverage portfolio improvement.
2. **Make the OpenHuman contribution record explicit.** Add a portfolio page grouping the 69 merged PRs into memory, RPC/controller architecture, privacy/security, reliability, and tests. Separately label personal-index branches as prototypes.
3. **Commit the Voice benchmark report.** Check in the external-corpus manifest, model/config hashes, WER and real-time-factor tables, failure categories, and one-command reproduction. This unlocks the stronger 560-clip/WER bullet.
4. **Publish a sanitized LiveLM evaluation report.** Preserve the 71 × 3 benchmark, 512 probes, status contract, latency distribution, and known limitations without exposing proprietary data.
5. **Reconcile HomeBase documentation with reality.** Update the root README and system design so implemented features, proof status, and unfinished work agree. Add a clean restart/evidence bundle before promoting it to Tier 1.
6. **Create a private Skild proof packet.** Record metric definitions, comparison windows, sample sizes, calculation methods, platform list, demo dates, and a reference who can corroborate the results.
7. **Refresh the GitHub profile and pins.** Lead with the reliability thesis and pin only projects that support it: Bridge case study, Voice, OfficeQA, Jarvis, the OpenHuman contribution page, and HomeBase only after repair.

## Tailoring switches

The master résumé should remain the source. Create role variants by swapping no more than 20–25% of the content.

| Role lane | Lead with | Swap in | De-emphasize |
|---|---|---|---|
| Agent reliability / infrastructure | Bridge, OpenHuman, LiveLM | HomeBase after repair, Axioms | Leadership detail |
| Evaluation / applied research | OfficeQA, LiveLM, OpenHuman | Jarvis evaluation metrics | Skild staffing details |
| Local inference / Apple platforms | Voice, Jarvis, OpenHuman | Inbox | Formal-method counts if space is tight |
| Robotics / physical AI | Skild, Voice | GemmaBot and verified robotics work | Personal-data integration |

## Maintenance rules

For every future metric, keep five fields: exact wording, denominator, measurement window, evidence path/URL, and last verification date. Never promote a claim from a branch, plan, or design document as shipped work. Prefer one exact result with a traceable artifact over three impressive but fragile numbers.

When a project changes, update this file first, then regenerate the tailored résumé. The master should always answer three questions quickly: **What systems did Jwalin build? What failed before? What evidence shows the new system is more reliable?**
