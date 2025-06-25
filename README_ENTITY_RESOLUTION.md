# Entity Resolution System

## Current State

**Problem**: 99 aliases point to a Person node with `null` name instead of connecting to actual named persons.

```cypher
// Current situation: All aliases point to null-named person
MATCH (alias:Alias)-[:ALIAS_OF]->(p:Person) 
WHERE p.name IS NULL 
RETURN count(*) as unresolved_aliases;
// Result: 99 unresolved aliases
```

**Goal**: Connect these aliases to actual named persons who already exist in the database.

## Alias Breakdown

```cypher
MATCH (alias:Alias) 
RETURN alias.type, count(*) as count 
ORDER BY count DESC;
```

- **40 nicknames**: @Eagle, William, @Hawk, Kenzie, etc.
- **24 phone numbers**: 9366351931, 9364254000, etc.  
- **18 email addresses**: ziezieken88@gmail.com, jadog83@gmail.com, etc.
- **17 IMEIs**: Device identifiers

## Entity Resolution Process

### Step 1: Find Unresolved Aliases

```cypher
// Show aliases needing resolution
MATCH (alias:Alias)-[:ALIAS_OF]->(p:Person) 
WHERE p.name IS NULL 
RETURN alias.type, alias.rawValue 
ORDER BY alias.type, alias.rawValue;
```

### Step 2: Identify Correct Person

```cypher
// Find who should own a specific phone number
MATCH (phone:Phone {number: '9366351931'})-[:PARTICIPATED_IN]->(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(other_device)<-[:USES]-(actual_person:Person)
WHERE actual_person.name IS NOT NULL
RETURN actual_person.name, count(s) as shared_sessions
ORDER BY shared_sessions DESC;
```

### Step 3: Create Resolution Rules

After investigation, write rules in `scripts/cypher/entity-resolution-rules.cypher`:

```cypher
// RULE 1: Connect William Eagle's phone alias to actual William
MATCH (alias:Alias {type: 'msisdn', rawValue: '9366351931'})
MATCH (william:Person {name: '@Eagle, William'})
MATCH (alias)-[old_rel:ALIAS_OF]->(null_person:Person)
WHERE null_person.name IS NULL
DELETE old_rel
MERGE (alias)-[:ALIAS_OF]->(william);
```

## Resolution Templates

### Template A: Phone Number Resolution

```
Investigation: "Phone 9366351931 communicates frequently with William Eagle's known phone"
Rule: Connect phone alias to William Eagle
```

```cypher
MATCH (alias:Alias {type: 'msisdn', rawValue: 'PHONE_NUMBER'})
MATCH (person:Person {name: 'PERSON_NAME'})
MATCH (alias)-[old_rel:ALIAS_OF]->(null_person:Person)
WHERE null_person.name IS NULL
DELETE old_rel
MERGE (alias)-[:ALIAS_OF]->(person);
```

### Template B: Email Resolution

```
Investigation: "Email ziezieken88@gmail.com appears in Kenzie's communications"
Rule: Connect email alias to Kenzie Hawk
```

```cypher
MATCH (alias:Alias {type: 'email', rawValue: 'EMAIL_ADDRESS'})
MATCH (person:Person {name: 'PERSON_NAME'})
MATCH (alias)-[old_rel:ALIAS_OF]->(null_person:Person)
WHERE null_person.name IS NULL
DELETE old_rel
MERGE (alias)-[:ALIAS_OF]->(person);
```

### Template C: Nickname Resolution

```
Investigation: "@Eagle, William nickname matches actual person William Eagle"
Rule: Connect nickname alias to William Eagle
```

```cypher
MATCH (alias:Alias {type: 'nickname', rawValue: 'NICKNAME'})
MATCH (person:Person {name: 'PERSON_NAME'})
MATCH (alias)-[old_rel:ALIAS_OF]->(null_person:Person)
WHERE null_person.name IS NULL
DELETE old_rel
MERGE (alias)-[:ALIAS_OF]->(person);
```

## Investigation Techniques

### Find Communication Partners

```cypher
MATCH (phone:Phone {number: 'UNKNOWN_PHONE'})-[:PARTICIPATED_IN]->(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(partner_device)<-[:USES]-(partner:Person)
WHERE partner.name IS NOT NULL
RETURN partner.name, count(s) as conversations
ORDER BY conversations DESC;
```

### Check Timing Correlations

```cypher
MATCH (ph1:Phone {number: 'PHONE1'})-[:PARTICIPATED_IN]->(s1:Session)
MATCH (ph2:Phone {number: 'PHONE2'})-[:PARTICIPATED_IN]->(s2:Session)
WHERE abs(duration.inSeconds(datetime(s1.starttime), datetime(s2.starttime)).seconds) < 300
RETURN count(*) as calls_within_5_minutes;
```

### Content Analysis for Names

```cypher
MATCH (phone:Phone {number: 'UNKNOWN_PHONE'})-[:PARTICIPATED_IN]->(s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.text CONTAINS 'william' OR c.text CONTAINS 'eagle'
RETURN substring(c.text, 0, 100) as content_sample
LIMIT 5;
```

## Execution Workflow

### 1. Apply Resolution Rules

```bash
# Apply all rules at once
docker exec -i neo4j-sessions cypher-shell -u neo4j -p Sup3rSecur3! < scripts/cypher/entity-resolution-rules.cypher
```

### 2. Verify Results

```cypher
// Check progress - should decrease from 99
MATCH (alias:Alias)-[:ALIAS_OF]->(p:Person) 
WHERE p.name IS NULL 
RETURN count(*) as remaining_unresolved;
```

```cypher
// Show successful resolutions
MATCH (alias:Alias)-[:ALIAS_OF]->(p:Person)
WHERE p.name IS NOT NULL
RETURN p.name, alias.type, count(*) as resolved_aliases
ORDER BY resolved_aliases DESC;
```

### 3. Test Specific Cases

```cypher
// Verify William Eagle's phones are properly connected
MATCH (william:Person {name: '@Eagle, William'})<-[:ALIAS_OF]-(alias:Alias {type: 'msisdn'})
RETURN alias.rawValue as williams_phones;
```

## Current Known Connections

Based on actual database investigation, these connections should be established:

- **William Eagle**: Phones 9366351931, 9364254000 (already connected via USES relationship)
- **Kenzie Hawk**: Phone 3032663434 (already connected), Email ziezieken88@gmail.com (connected to @Kenzie Hawk)
- **Note**: The USES relationships already exist between Person and Phone/Email nodes
- **Issue**: Alias nodes still point to null-named Person instead of actual named persons

## Complete Resolution Example

**1. Find unresolved phone alias:**

```cypher
MATCH (alias:Alias {type: 'msisdn', rawValue: '9366351931'})-[:ALIAS_OF]->(p:Person)
RETURN p.name; // Returns: null
```

**2. Investigate ownership:**

```cypher
MATCH (phone:Phone {number: '9366351931'})-[:PARTICIPATED_IN]->(s:Session)
MATCH (s)<-[:PARTICIPATED_IN]-(other)<-[:USES]-(known:Person)
WHERE known.name IS NOT NULL
RETURN known.name, count(s) ORDER BY count(s) DESC;
// Result: @Eagle, William (77 shared sessions)
```

**3. Create rule:**

```cypher
MATCH (alias:Alias {type: 'msisdn', rawValue: '9366351931'})
MATCH (william:Person {name: '@Eagle, William'})
MATCH (alias)-[old_rel:ALIAS_OF]->(null_person:Person)
WHERE null_person.name IS NULL
DELETE old_rel
MERGE (alias)-[:ALIAS_OF]->(william);
```

**4. Verify:**

```cypher
MATCH (alias:Alias {type: 'msisdn', rawValue: '9366351931'})-[:ALIAS_OF]->(p:Person)
RETURN p.name; // Should return: @Eagle, William
```

## Repeatability

After database rebuilds:

1. **Load initial data** (creates 99 unresolved aliases)
2. **Execute resolution rules** from `scripts/cypher/entity-resolution-rules.cypher`
3. **Verify results** using validation queries
4. **Test evaluations** to ensure system functionality

This process transforms unresolved aliases into proper person-identifier relationships, enabling all evaluation tests to pass consistently.