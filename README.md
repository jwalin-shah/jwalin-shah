<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hero-dark.svg" />
  <img src="hero-light.svg" alt="Jwalin Shah — Reliable agent systems, measured end to end." width="900" />
</picture>

</div>

I build systems that make probabilistic agents inspectable and dependable: isolated execution, deterministic verification, grounded retrieval, evaluation infrastructure, and fully local inference.

`69 merged upstream PRs` · `77 documented invariants` · `4,400+ evaluations` · `5 robotics platforms`

[**Portfolio**](https://jwalin-shah.github.io) · [**Resume**](https://github.com/jwalin-shah/jwalin-shah/raw/main/Jwalin_Shah_Resume_General.pdf) · [**LinkedIn**](https://linkedin.com/in/jwalin-shah) · [**Email**](mailto:jwalinshah13@gmail.com)

---

### Selected systems

**1. [OpenHuman](https://github.com/tinyhumansai/openhuman)** — *Active · upstream*  
Personal-memory / ingest in the Rust core: hybrid FTS5 + sqlite-vec retrieval, staged iMessage/Gmail/Calendar/Contacts ingest, contact identity via CNContactStore, and production hardening around citations, RPC, privacy/security, and chat reliability.

**2. [voice-engine-swift](https://github.com/jwalin-shah/voice-engine-swift)** — *Active · local product*  
Fully local dictation (Moonshine + CoreML). Bench: 26 ASR configs · 560 clips · moonshine-tiny **0.2177 WER / 0.05 RTF** vs canary-qwen-2.5B **0.2162 / 0.73** — same accuracy class, **14× lower RTF**. Tests: **62/62** v0.1 acceptance · **348/349** full regression (one CoreML OS regression documented).

**3. [officeqa-arena](https://github.com/jwalin-shah/officeqa-arena)** — *Completed case study*  
Sentient Cohort 0 grounded QA: **184.5/246 (75%)** at \$1.71 · ~4,400 evaluations. Evidence selection caused 48% of failures; correctly grounded Python had 0% arithmetic errors. [research.pdf](https://github.com/jwalin-shah/officeqa-arena/blob/main/research.pdf).

**4. Bridge** — *Private architecture* · [sanitized overview →](https://github.com/jwalin-shah/bridge-architecture)  
Spawn → verify → deliver for coding agents: deny-default sandboxing, leased worktrees, fresh-checkout verification. **77 invariants** with property tests + TLA+ / Z3 / Lean. Public write-up linked above; implementation stays private.

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="stats-dark.svg" />
  <img src="stats-light.svg" alt="Proof of work strip: 69 PRs, 77 invariants, 4,400+ evaluations, on-device + 5 robot platforms." width="900" />
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
