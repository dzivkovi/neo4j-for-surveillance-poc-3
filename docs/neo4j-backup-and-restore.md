# Neo4j Backup and Restore Guide

**Last Updated:** 2025-07-17  
**Applies to:** Neo4j Community Edition with Docker

## Overview

This guide covers the standard backup method for Neo4j databases using `neo4j-admin database dump`.
This creates portable .dump files that can be restored on any Neo4j 5.x instance.

## Creating a Database Backup

### Automated Script (Recommended)

```bash
# Use the backup script for any dataset
./scripts/backup-neo4j.sh ${DATASET}

# Examples:
./scripts/backup-neo4j.sh gantry        # Creates: data/gantry/neo4j-database-TIMESTAMP.dump
./scripts/backup-neo4j.sh whiskey-jack  # Creates: data/whiskey-jack/neo4j-database-TIMESTAMP.dump
```

**What happens:**
1. Container stops briefly (required for Community Edition)
2. Creates timestamped dump file
3. Container automatically restarts
4. Shows restore instructions

### Manual Process

If you need to create a dump manually:

```bash
# 1. Stop the container
docker stop neo4j-${DATASET}

# 2. Create the dump
docker run --rm \
  --volumes-from neo4j-${DATASET} \
  -v $(pwd)/data/${DATASET}:/backup:rw \
  neo4j:5.26.7-community \
  bash -c "neo4j-admin database dump neo4j --to-stdout > /backup/neo4j-database-$(date +%Y-%m-%d_%H%M%S).dump"

# 3. Restart the container
docker start neo4j-${DATASET}
```

## Restoring from a Database Dump

```bash
# 1. Stop the target container
docker stop neo4j-${DATASET}

# 2. Load the dump (overwrites existing data)
docker run --rm \
  --volumes-from neo4j-${DATASET} \
  -v $(pwd)/path/to/dump.file:/dump.file \
  neo4j:5.26.7-community \
  neo4j-admin database load neo4j --from-stdin --overwrite-destination < /dump.file

# 3. Start the container
docker start neo4j-${DATASET}
```

### Example: Restoring whiskey-jack dataset

```bash
# Stop container
docker stop neo4j-whiskey-jack

# Load specific dump
docker run --rm \
  --volumes-from neo4j-whiskey-jack \
  -v $(pwd)/data/whiskey-jack/neo4j-database-2025-07-17_162849.dump:/dump.file \
  neo4j:5.26.7-community \
  neo4j-admin database load neo4j --from-stdin --overwrite-destination < /dump.file

# Start container
docker start neo4j-whiskey-jack
```

## Memory Configuration for Large Datasets

For datasets with 250K+ nodes (like the gantry case):

```bash
# Container memory limits
--memory=8g --memory-swap=8g

# Neo4j heap memory (handles queries)
-e NEO4J_server_memory_heap_initial__size=4G
-e NEO4J_server_memory_heap_max__size=4G

# Page cache (stores graph data)
-e NEO4J_server_memory_pagecache_size=4G

# Additional settings for stability
-e NEO4J_db_transaction_timeout=120s
-e NEO4J_db_lock_acquisition_timeout=120s
```

## Important Notes

1. **Portability**: Dumps are portable across Neo4j 5.x instances
2. **Downtime**: Community Edition requires brief downtime during backup
3. **File Naming**: Always use timestamped filenames to avoid confusion
4. **Storage**: Dump sizes vary by dataset (whiskey-jack: ~2MB, gantry: ~3GB)

## Best Practices

1. **Regular Backups**: Daily snapshots, weekly dumps
2. **Test Restores**: Verify backups work before you need them
3. **Storage Management**: Remove old snapshots to save disk space
4. **Document Versions**: Include date in backup names

## Troubleshooting

### OutOfMemoryError
- Increase Docker Desktop memory to 10+ GB
- Use memory-optimized settings shown above
- Monitor with: `docker stats neo4j-${CASENAME}`

### Container Stops When Neo4j Stops
- This is normal for Community Edition
- Use snapshots for online backups
- Schedule dumps during maintenance windows

### Restore Performance
- Add performance indexes after restore (see `scripts/01-create-schema.sh`)
- Allow Neo4j to warm up cache after restart
- First queries may be slower until cache populates