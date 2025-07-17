# Neo4j Backup and Restore Guide

**Last Updated:** 2025-07-16  
**Applies to:** Neo4j Community Edition with Docker

## Overview

This guide covers two backup methods for Neo4j databases:
1. **Docker Snapshots** (Recommended for quick backup/restore)
2. **Database Dumps** (For data portability and archival)

## Method 1: Docker Snapshots (Fastest)

### Creating a Backup

```bash
# Generic pattern
docker commit neo4j-${CASENAME} neo4j-${CASENAME}-snapshot:$(date +%Y-%m-%d)

# Example for 'gantry' case
docker commit neo4j-gantry neo4j-gantry-snapshot:2025-07-16
```

**What's included:**
- All data and indexes
- All configurations
- Installed plugins (APOC, GDS)
- Memory settings

### Listing Backups

```bash
# View all snapshots
docker images | grep neo4j-.*-snapshot

# Example output:
# neo4j-gantry-snapshot   2025-07-16   0c84df0f3d9d   5.38GB
# neo4j-gantry-snapshot   2025-07-14   e932c92fb0dd   2.75GB
```

### Restoring from Snapshot

```bash
# Stop current container if running
docker stop neo4j-${CASENAME} && docker rm neo4j-${CASENAME}

# Restore with optimized memory settings
docker run -d \
  --name neo4j-${CASENAME} \
  --memory=8g --memory-swap=8g \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_server_memory_heap_initial__size=4G \
  -e NEO4J_server_memory_heap_max__size=4G \
  -e NEO4J_server_memory_pagecache_size=4G \
  neo4j-${CASENAME}-snapshot:2025-07-16

# Example for 'gantry' case
docker run -d \
  --name neo4j-gantry \
  --memory=8g --memory-swap=8g \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_server_memory_heap_initial__size=4G \
  -e NEO4J_server_memory_heap_max__size=4G \
  -e NEO4J_server_memory_pagecache_size=4G \
  neo4j-gantry-snapshot:2025-07-16
```

## Method 2: Database Dumps (Portable)

### Creating a Dump (Offline Method - What Actually Works)

**Note:** Neo4j Community Edition requires stopping the database to create dumps.

```bash
# 1. Stop the Neo4j container (this stops the database)
docker stop neo4j-${CASENAME}

# 2. Create a temporary container to access the stopped data
docker run --rm \
  --volumes-from neo4j-${CASENAME} \
  -v $(pwd)/data/${CASENAME}:/backup \
  neo4j:5.26.7-community \
  neo4j-admin database dump neo4j --to-stdout > data/${CASENAME}/neo4j-database-$(date +%Y-%m-%d).dump

# 3. Restart the original container
docker start neo4j-${CASENAME}

# Example for gantry case:
docker stop neo4j-gantry
docker run --rm \
  --volumes-from neo4j-gantry \
  -v $(pwd)/data/gantry:/backup \
  neo4j:5.26.7-community \
  neo4j-admin database dump neo4j --to-stdout > data/gantry/neo4j-database-2025-07-16.dump
docker start neo4j-gantry
```

This creates a dump file like: `data/gantry/neo4j-database-2025-07-16.dump` (628MB for our dataset)

### Restoring from Dump

```bash
# 1. Copy dump into container
docker cp data/${CASENAME}/neo4j-database-YYYY-MM-DD.dump \
  neo4j-${CASENAME}:/var/lib/neo4j/import/

# 2. Load the dump
docker exec neo4j-${CASENAME} \
  neo4j-admin database load neo4j \
  --from-stdin < data/${CASENAME}/neo4j-database-YYYY-MM-DD.dump \
  --overwrite-destination=true

# 3. Restart container
docker restart neo4j-${CASENAME}
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
-e NEO4J_db_tx__timeout=120s
-e NEO4J_db_lock_acquisition_timeout=120s
```

## Automated Backup Script

See `scripts/backup-neo4j.sh` for automated daily backups.

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