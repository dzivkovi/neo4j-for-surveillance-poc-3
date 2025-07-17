# Scripts Directory

This directory contains the operational scripts that power the Neo4j surveillance analytics system.

## Structure

- **`python/`** - Data processing, embedding generation, and evaluation automation
- **`cypher/`** - Database schema, validation, and maintenance queries

## Usage

**For setup and operational commands**, see the main project documentation:

- [README.md](../README.md) - Complete setup instructions and essential commands
- [CLAUDE.md](../CLAUDE.md) - Development commands and operational procedures

## Philosophy

Scripts are organized by technology (Python vs Cypher) rather than function to minimize cognitive load and follow the project's design principle: *"Optimize for User Interaction Pattern"*.

Database administrators work with Cypher files, Python developers work with Python files, and both can focus on their domain without cross-technology context switching.

## Maintenance

This directory structure is intentionally stable - scripts may change but the organization remains constant. Individual script documentation is maintained in the files themselves and the main project README.