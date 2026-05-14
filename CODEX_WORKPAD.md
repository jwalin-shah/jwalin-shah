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

## Slice: shallow module deepening - WP-079

Branch: `codex/WP-079-shallow-module-deepening`

Deepened `scripts/validate_publication.py` by moving claim loading, README
reference parsing, SVG aria checks, and required link checks behind
`PublicationValidator`. The public caller surface remains `validate_publication(root)`,
and the existing failure probe now exercises that module entry point rather than
separate helper trivia.

Validation:

```bash
python3 scripts/validate_publication.py
git diff --check
```

Result: passed.

## Slice: CLI smoke contract - WP-135

Branch: `codex/WP-135-cli-smoke-contract`

Added a narrow argparse surface to `scripts/validate_publication.py`:

- default validation still checks the current repo, stale-SVG failure reporting,
  and now the no-secret CLI smoke contract
- `--smoke --root <path>` runs a cheap entrypoint check against a supplied root
- missing roots now fail clearly with `publication validation failed: missing README.md ...`

Validation:

```bash
python3 scripts/validate_publication.py
python3 scripts/validate_publication.py --smoke --root /tmp/does-not-exist-wp135
git diff --check
```

Result: publication validation passed; bad-root smoke exited 1 with a clear
failure message; diff check passed.

## Slice: fixture/runtime separation - WP-163

Branch: `codex/WP-163-fixture-runtime-separation`

Separated generated validator self-test fixtures from tracked evidence:

- `.runtime/` is ignored for local generated output.
- `scripts/validate_publication.py` defaults generated self-test fixture roots to
  `.runtime/publication-validator/` and asserts that default in the CLI smoke
  contract.
- `docs/status/README.md` documents `docs/status/` as curated tracked evidence,
  not a default runtime-output target.

Validation:

```bash
python3 scripts/validate_publication.py
git diff --check
```

Result: passed.

## Slice: error boundary hardening - WP-191

Branch: `codex/WP-191-error-boundary-hardening`

Hardened the `public_claims.json` parser boundary in
`scripts/validate_publication.py` so malformed claims schema fails closed with
deterministic validation errors before downstream comparison logic can produce
misleading output. Added a negative self-test fixture for `required_links`
provided as a string instead of a list.

Validation:

```bash
python3 scripts/validate_publication.py
git diff --check
```

Result: passed.

## WP-051: README image parser regression - 2026-05-14

Added focused regression probes for README image alt text where the `alt`
attribute appears before `src`, and for `<img>` tags missing alt text. The old
regex parser missed that `<img>` shape when a matching `<source>` kept the image
set otherwise valid, allowing stale README alt text to pass.

Updated `scripts/validate_publication.py` to parse README image tags with
`html.parser.HTMLParser` inside the current `PublicationValidator` structure, so
`<source srcset>` and `<img src alt>` references are checked independent of
attribute order.

Validation:

```bash
python3 scripts/validate_publication.py
```

Result: passed.
