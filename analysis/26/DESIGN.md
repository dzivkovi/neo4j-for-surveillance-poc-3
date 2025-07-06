# Neo4j Dataset‑Specific Docker Containers

## Problem / Metric

Current workflow launches **one** Neo4j container (`neo4j‑sessions`) and reloads data for every benchmark run. Reloading takes ≈ 3–4 minutes, slows feedback loops, and risks human error.

*Metric*: Switching datasets must take **< 10 seconds** (stop → start) with **zero data loss** across container restarts.

---

## Goal

Enable developers to spin up **dataset‑specific** Neo4j containers (e.g. `neo4j-default`, `neo4j-bigdata`) on Docker Desktop/Windows using the same image and host ports, where only one container runs at a time.

---

## Scope (M/S/W)

- **[M]** Parameterise container name with a `DATASET` argument or env‑var and derive `$NEO_NAME="neo4j-${DATASET}"`.
- **[M]** Provide Bash helper `run_neo4j.sh` that:
  - Stops any container currently bound to port 7474 if running (convenience only).
  - Launches a new container with the computed name and standard ports (7474/7687).
- **[M]** Update **README.md** commands to use `$NEO_NAME` instead of the hard‑coded `neo4j-sessions`.
- **[M]** **Update CLAUDE.md** to adopt the same `$NEO_NAME` pattern and include `run_neo4j.sh` in its *Essential Commands*.
- **[M]** Replace **all** remaining `neo4j-sessions` literals in *other markdown files and scripts* (docs folder, root, sub‑scripts).  Use `rg -l 'neo4j-sessions'` to list affected files during refactor.
- **[M]** Ensure writable layer (graph DB) survives `docker stop / start`.
- **[S]** Optional snapshot command (`docker commit`) documented for freezing a dataset.
- **[W]** Running multiple containers concurrently on different ports.
- **[W]** Volume mounts for external persistence.
- **[W]** Orchestration with Docker Compose / Kubernetes.

---

## Design Details

### Environment variables

```bash
export DATASET=${DATASET:-default}          # e.g. default | bigdata | clientA
export NEO_NAME="neo4j-${DATASET}"
```

### Helper script (`run_neo4j.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail
DATASET=${1:-default}
NEO_NAME="neo4j-${DATASET}"

# Convenience: stop any container already bound to 7474/7687
RUNNING=$(docker ps --filter publish=7474 --format '{{.Names}}')
[ -n "$RUNNING" ] && docker stop "$RUNNING"

docker run --name "$NEO_NAME" \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Sup3rSecur3! \
  -e NEO4J_PLUGINS='["apoc","graph-data-science","genai"]' \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*,db.*,genai.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*,db.*,genai.* \
  -d neo4j:5.26.7-community
```

### Optional snapshot pattern

```bash
# Freeze current state
docker stop $NEO_NAME
docker commit $NEO_NAME ${NEO_NAME}:snap-$(date +%Y-%m-%d)
```

---

## Documentation Updates

1. **README.md** – prepend the environment‑variable snippet and change all commands to `$NEO_NAME`.
2. **CLAUDE.md** – same updates plus add `./run_neo4j.sh <dataset>` to *Neo4j Operations*.
3. **Other markdown / scripts** – search‑and‑replace every literal `neo4j-sessions`; verify with `rg -l 'neo4j-sessions'`.

> **Principle**: *No literal **``** should remain anywhere in the repo.* Always reference the container via `$NEO_NAME`.

---

## Acceptance Criteria

| # | Given                                              | When                                                  | Then                                                                                  |
| - | -------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 1 | No container is running on port 7474               | Developer runs `./run_neo4j.sh default`               | Container **neo4j-default** starts and maps 7474/7687                                 |
| 2 | **neo4j-default** is running                       | Developer executes `docker stop neo4j-default`        | Container exits (status *Exited*) and its data is preserved                           |
| 3 | **neo4j-default** is stopped                       | Developer runs `./run_neo4j.sh bigdata`               | Script auto‑stops any running container on 7474 (none), then starts **neo4j-bigdata** |
| 4 | **neo4j-bigdata** contains imported data           | Developer stops and restarts it (`docker stop/start`) | Dataset remains intact (Cypher count equals pre‑stop value)                           |
| 5 | A container named **neo4j-default** already exists | Developer reruns `./run_neo4j.sh default`             | Script fails clearly or prompts to remove existing container                          |
| 6 | README updated                                     | Reviewer follows README on a clean machine            | Workflow executes without modification and meets timing metric (<10 s switch)         |
| 7 | **CLAUDE.md** updated                              | Reviewer follows any command block in CLAUDE.md       | All commands work with `$NEO_NAME`; no literal `neo4j-sessions` remains               |
| 8 | **Other markdown / scripts** updated               | Reviewer runs `rg -l 'neo4j-sessions'` at repo root   | Command returns **no files**, confirming all literals removed                         |

---

## Out‑of‑Scope

- Production‑grade volume backups (named volumes, restic, cloud snapshots).
- Automated dataset import on every container start (handled by existing loader scripts).

