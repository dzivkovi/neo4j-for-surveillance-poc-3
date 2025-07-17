# Repository Documentation Cleanup

## Problem / Metric

> Root directory has 10+ `README_*` files that overwhelm first-time visitors.  
> **Metric to move:** reduce top-level Markdown files from 11 → 2 (README.md, CONTRIBUTING.md).

## Goal

Present a minimal, intuitive file tree so newcomers grasp the project in < 30 seconds.

## Scope (M / S / W)

- **[M]** Create `docs/` folder.
- **[M]** Move or merge every auxiliary `README_*.md` into `docs/`.
- **[M]** Keep root `README.md` ≤ 150 lines (intro + quick-start + dir map).
- **[M]** Add shebang line to every script in `scripts/`.
- **[S]** Merge `README_cypher-shell.md` content into `docs/import.md`.
- **[S]** Add bullet to `CONTRIBUTING.md` about branch/title prefix.
- **[W]** Modify code logic, tests, or CI pipelines.

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Fresh clone | ls -1 in root | Shows only `README.md`, `CONTRIBUTING.md`, `docs/`, `analysis/`, `evals/`, `scripts/`, `.github/`, `pyproject.toml` |
| 2 | In root | open `README.md` | ≤ 150 lines, links to each `docs/*` topic |
| 3 | In `docs/` | count Markdown files | ≥ 6 topic files listed below |
| 4 | For each root script | open first line | Starts with `#!/usr/bin/env` shebang |
| 5 | Run `grep -R README_ .` | Returns **no** matches outside `docs/` |

### Topic files expected in `docs/`

- `import.md`
- `evaluations.md`
- `lucene.md`
- `case-study.md`
- `kanban.md`
- `claude-automation.md`

## Risks / Blockers / Owner

- **Risk:** Broken links in existing issues/PRs → run `grep -R "README_"` and patch.  
- **Owner:** Daniel (repo maintainer).
