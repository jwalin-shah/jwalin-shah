# Portfolio Readiness Reconciliation - 2026-05-12

Scope: presentation-track slice for the workspace-wide portfolio readiness goal.

## Live Status

- Branch: `main`
- Dirty surface before this slice: generated architecture docs and `.gitignore`
- Additional readiness edits in this slice:
  - aligned `hero-*.svg` aria labels with README alt text
  - aligned `stats-*.svg` aria labels with the visible stats/README claim
  - added `scripts/validate_publication.py`

## Finding

The profile README claimed the stats image as:

- Python 80%
- TypeScript 9%
- JavaScript 3%
- Svelte 3%
- Shell 3%
- Other 2%

Both stats SVG aria labels instead summarized it as Python 81%, TypeScript 6%,
Other 13%. That made the public accessibility text inconsistent with the
visible graphic and README.

## Validation

```bash
python3 scripts/validate_publication.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Fresh Publication Validation - 2026-05-13

Validation:

```bash
python3 scripts/validate_publication.py
git diff --check
```

Result: passed.

## Next Handoff

- Keep `scripts/validate_publication.py` as the publication gate for README
  image references, SVG aria labels, and required public links.
- Next profile issue can extend the same gate into a canonical claims file
  before regenerating SVGs from shared templates.

## Slice: canonical claims source - 2026-05-12

Added `public_claims.json` and updated `scripts/validate_publication.py` so
README image alt text, SVG aria labels, and required public links are checked
against the repo-local claims file.

Validation:

```bash
python3 scripts/validate_publication.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.
