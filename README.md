<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hero-dark.svg" />
  <img src="hero-light.svg" alt="Jwalin Shah — Reliable agent systems, measured end to end." width="900" />
</picture>

</div>

I build systems that make probabilistic agents inspectable and dependable: isolated execution, deterministic verification, grounded retrieval, evaluation infrastructure, and fully local inference.

[**Portfolio**](https://jwalin-shah.github.io) · [**Resume**](https://github.com/jwalin-shah/jwalin-shah/raw/main/Jwalin_Shah_Resume_General.pdf) · [**LinkedIn**](https://linkedin.com/in/jwalin-shah) · [**Email**](mailto:jwalinshah13@gmail.com)

---

### Systems and evidence

**1. [OpenHuman](https://github.com/tinyhumansai/openhuman)** — *Active · upstream*  
Personal memory and ingest in the Rust core: hybrid FTS5 + sqlite-vec retrieval, staged iMessage/Gmail/Calendar/Contacts ingest, contact identity via CNContactStore, and production hardening around citations, RPC, privacy/security, and chat reliability. [[69 merged upstream PRs](https://github.com/tinyhumansai/openhuman/pulls?q=is%3Apr+author%3Ajwalin-shah+is%3Amerged)]

**2. [voice-engine-swift](https://github.com/jwalin-shah/voice-engine-swift)** — *Active · local product*  
Fully local dictation (Moonshine + CoreML). Bench: 26 ASR configs · 560 clips · moonshine-tiny **0.2177 WER / 0.05 RTF** vs canary-qwen-2.5B **0.2162 / 0.73** — same accuracy class, **14× lower RTF**. Tests: **62/62** v0.1 acceptance · **348/349** full regression (one CoreML OS regression documented).

**3. [officeqa-arena](https://github.com/jwalin-shah/officeqa-arena)** — *Completed case study*  
Sentient Cohort 0 grounded QA: **184.5/246 (75%)** at \$1.71 · ~4,400 evaluations. Evidence selection caused 48% of failures; correctly grounded Python had 0% arithmetic errors. [research.pdf](https://github.com/jwalin-shah/officeqa-arena/blob/main/research.pdf).

**4. Bridge** — *Private architecture* · [sanitized overview + runnable lease slice →](https://github.com/jwalin-shah/bridge-architecture)  
Spawn → verify → deliver for coding agents: deny-default sandboxing, leased worktrees, fresh-checkout verification. Public repo ships one inspectable assurance slice (TLA+ + Go property test + CI); full catalog stays private.

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="stats-dark.svg" />
  <img src="stats-light.svg" alt="Capability strip: Rust+Go production core, Swift+CoreML local ASR, TLA+/Z3/Lean formal assurance, robotics ops across 5 platforms." width="900" />
</picture>

</div>

---

### Background

| | |
|---|---|
| **OpenHuman** (tinyhumansai) | Core contributor — personal memory, ingest, hybrid retrieval |
| **Break the Web / LiveLM** | AI Systems Engineer — grounded retrieval, MCP, ChatGPT path, eval harnesses |
| **Skild AI** | Data Operations Lead — 5 robotic platforms · eval/ops systems · Series C demos |

### Contact

Open to **agent reliability**, **evaluation infrastructure**, and **local-first systems** roles.  
✉️ [jwalinshah13@gmail.com](mailto:jwalinshah13@gmail.com) · 🌐 [portfolio](https://jwalin-shah.github.io) · 💼 [linkedin](https://linkedin.com/in/jwalin-shah)
