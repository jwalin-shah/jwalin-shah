# Status Artifacts

This directory holds curated, deterministic publication-status evidence that is
intended to stay in version control.

Do not use `docs/status/` as the default target for generated validator logs,
scratch fixtures, or local run output. Runtime output belongs under the ignored
`.runtime/` tree; `scripts/validate_publication.py` defaults its generated
self-test fixtures to `.runtime/publication-validator/`.
