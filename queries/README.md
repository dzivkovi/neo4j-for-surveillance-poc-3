# Investigative Queries

This directory contains **surveillance analytics queries** for law enforcement investigators and analysts conducting case work.

## Purpose

Unlike operational scripts that maintain the system, these queries are designed for **active investigations** and **case analysis**. They represent the business value of the surveillance analytics platform - turning raw communication data into actionable intelligence.

## Query Categories

- **`investigative.cypher`** - Core investigative queries for suspect tracking and evidence correlation
- **`practical-investigation-queries.cypher`** - Real-world case scenarios and analysis patterns
- **`eval-suite.cypher`** - Business requirement validation (77 investigative questions)
- **`data-exploration.cypher`** - Discovery queries for understanding dataset scope and content
- **`graph-visualization-examples.cypher`** - Network analysis and relationship mapping
- **`vector-search-verification.cypher`** - Semantic search capabilities for content analysis

## Target Users

**Surveillance Analysts** - Finding evidence, tracking suspects, mapping networks
**Investigators** - Building cases, correlating communications, timeline analysis  
**Intelligence Teams** - Pattern recognition, relationship discovery, threat assessment

## Key Capabilities

- **Multi-identifier tracking** - Phone numbers, emails, IMEIs across suspects
- **Content analysis** - Semantic search through call transcripts and messages
- **Network mapping** - Communication patterns and relationship strength
- **Timeline reconstruction** - Temporal analysis of suspect activities
- **Evidence correlation** - Cross-referencing mentions, locations, and activities

## Distinction from Scripts

**`queries/`** = **Investigative/Analytical** - What analysts run to solve cases
**`scripts/`** = **Operational/Infrastructure** - What developers run to maintain the system

This separation ensures investigators can focus on case work without being overwhelmed by technical maintenance queries.

## Usage

These queries are designed to be executed against live surveillance data for active investigations. They assume the Neo4j database is populated with communication sessions, content, and relationship data following the POLE (Person, Object, Location, Event) schema.

**For system setup and maintenance**, see `scripts/` directory instead.

## Proven Investigative Capabilities

### 🎯 **Multi-Identifier Network Mapping**
**EVAL-43: "Who are William Eagle's top associates?"**
- **Results**: Richard Eagle (29 sessions), Fred Merlin (16 sessions), Kenzie Hawk (12 sessions)
- **Intelligence Value**: Reveals organizational hierarchy and communication frequency patterns
- **Graph Advantage**: Single query vs 6+ complex SQL JOINs through person→phone→session chains

### 🌐 **Cross-Platform Digital Footprint Analysis** 
**EVAL-77: Complete communication profile across email, SMS, telephony**
- **Kenzie's Network**: 16 unique email contacts, 56 total sessions
- **Pattern Analysis**: 57% personal vs 43% commercial communications
- **Priority Target**: jadog83@gmail.com identified (39% of all email traffic)

### 🔍 **Semantic Evidence Discovery**
**EVAL-05: "What is in the shed?" - High confidence results**
- **Evidence Found**: Rock salt storage, surveillance concerns, neighbor complaints
- **Traditional Database Limitation**: Keyword search misses contextual discussions
- **Investigation Value**: Discovers evidence through meaning, not just word matching

### ⏱️ **Timeline Reconstruction for Conspiracy Evidence**
**EVAL-16: Sago palms escalation pattern (Feb 9-11, 2020)**
- **Day 1**: William orders 2 palms ($45 each)
- **Day 2**: Richard calls it "extreme" 
- **Day 3**: Order escalated to 6 palms
- **Legal Value**: Demonstrates premeditation and conspiracy elements

### 🕷️ **Hidden Network Connections**
**Shortest Path Analysis: Beverly Eagle → Ray (6 degrees of separation)**
- **Network Influence**: Kenzie Hawk reaches 19 people within 3 degrees
- **Isolated Actors**: Owen Frasier only reaches 2 people (operational security indicator)
- **Investigation Insight**: Identifies key brokers vs isolated cells in criminal networks

### 🌍 **International Operations Support**
**EVAL-02: Multi-language investigation capability**
- **French Processing**: 29 travel-related discussions with semantic similarity
- **Cross-Language Evidence**: Same investigation across multiple languages
- **National Security Value**: Critical for trafficking, terrorism, organized crime

## System Performance Metrics

- **Query Speed**: Efficient response for complex network analysis
- **Reliability**: 94% success rate on core investigative functions (56/59 tests)
- **Current Scale**: 265 communication sessions, 251 transcripts with AI embeddings
- **Language Support**: English content with cross-language query capability
- **Platform Coverage**: Email, SMS, telephony with relationship strength analysis

## National Security Applications

### **Proof-of-Concept with Production Potential**
- **Architecture Reusability**: Same POLE schema works for any criminal network type
- **Rapid Deployment**: Docker compose → import data → analyze networks
- **Investigation-Agnostic Design**: Supports drug trafficking, terrorism, organized crime, cybercrime
- **Cross-Case Correlation Capability**: Foundation for connecting related criminal activities

### **Why Graph Databases Are Superior for National Security**
1. **Variable-length path queries** find hidden connections impossible in traditional databases
2. **Real-time relationship visualization** for operational intelligence
3. **Multi-hop traversal performance** scales linearly while SQL degrades exponentially
4. **Semantic search with relationship context** for evidence discovery
5. **Investigation domain agnostic** - works for any criminal network topology

*This proof-of-concept demonstrates the foundation for transforming manual investigative correlation into automated intelligence analysis.*
