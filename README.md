## Jwalin Shah

**AI Systems Engineer** — Evaluation & Reliability · Tool-Augmented Reasoning · Privacy-First Systems

Building systems to measure, diagnose, and improve LLM behavior. Currently focused on grounded reasoning, deterministic computation, and real-world AI reliability.

### Current Work

- **[OfficeQA Arena](https://github.com/jwalin-shah/officeqa-arena)** — Multi-agent LLM system ranking top tier (180+) on a 246-task financial benchmark. Demonstrated that retrieval errors and tool selection—not model reasoning—drive the majority of failures. Built evaluation infrastructure across 3,600+ tasks with telemetry for failure mode analysis (tool thrashing, temporal misalignment, retrieval errors).

- **[Jarvis](https://github.com/jwalin-shah/jarvis-ai-assistant)** — Privacy-first AI assistant on Apple Silicon (8GB M2 MacBook Air): MLX inference, hybrid retrieval (BM25 + embeddings + cross-encoder), zero cloud dependencies. Dual-path architecture: fast-path (<0.42s) for simple queries, background pipeline for complex grounded reasoning. Evaluation harness across 37 model configs optimizing latency, retrieval quality (Hit@5), and hallucination rates (<5%).

- **[Inbox](https://github.com/jwalin-shah/inbox)** — Unified terminal TUI consolidating iMessage, Gmail, Google Calendar, Apple Notes, Reminders, GitHub, and Google Drive. Client-server architecture (FastAPI) with local ML stack: MLX Whisper for ambient transcription, Qwen 3.5 0.8B for constrained generation. Optimistic UI with background confirmation.

- **[Personal Data Engine](https://github.com/jwalin-shah/data-connect-framework)** — Schema-driven ingestion framework for heterogeneous personal datasets. Canonical entity/event modeling with privacy-safe export lanes. SQLite + sqlite-vec backend.

- **[Squat Coach](https://github.com/jwalin-shah/squat-coach)** — Real-time biomechanics analysis using MediaPipe pose estimation + temporal smoothing for joint angle tracking on consumer hardware.

- **[OpenEnv](https://github.com/jwalin-shah/robo-replan)** — Custom RL environment with FastAPI state transitions and multi-dimensional reward. GRPO training achieving ~80% success baseline on tabletop robot planning tasks.

### Focus Areas

Grounded LLM reasoning · Evaluation harnesses & telemetry · Deterministic computation pipelines · Tool-augmented agents · Hallucination measurement & mitigation · On-device inference (MLX/Apple Silicon) · Privacy-first architectures · Robotics systems reliability

### Professional Background

**Sentient Arena (Cohort 0)** — Research Contributor: Grounded financial reasoning, evaluation infrastructure, failure mode analysis  
**Skild AI** — Data Operations Lead: Robotics data systems at scale (5 platforms, 25+ operators), task success +40%, overhead -50%

### Links

📊 [Resume](https://github.com/jwalin-shah) · 💼 [LinkedIn](https://linkedin.com/in/jwalin-shah) · 📧 jwalinshah13@gmail.com
