// Step 6: Analyst Knowledge Aliases (MANUAL TEMPLATE)
// This file contains investigation-specific name variations discovered through analysis
// Copy this template to case-specific file and customize before execution

// Example: Connect "Freddie" variations to canonical "Fred" entity
MATCH (p:Person {name: '@Merlin, Fred'})
MERGE (alias:Alias {rawValue: 'Freddie', canonical: p.name})
SET alias.type = 'nickname',
    alias.confidence = 'high',
    alias.analyst_notes = 'Common nickname variation - analyst knowledge',
    alias.created_date = datetime()
MERGE (p)-[:KNOWN_AS]->(alias);

// Template for adding more aliases:
// MATCH (p:Person {name: '@LastName, FirstName'})
// MERGE (alias:Alias {rawValue: 'variation', canonical: p.name})
// SET alias.type = 'nickname|misspelling|abbreviation',
//     alias.confidence = 'high|medium|low',
//     alias.analyst_notes = 'description',
//     alias.created_date = datetime()
// MERGE (p)-[:KNOWN_AS]->(alias);

// Example additional aliases for reference:
// MATCH (p:Person {name: '@Eagle, William'})
// MERGE (alias:Alias {rawValue: 'Bill', canonical: p.name})
// SET alias.type = 'nickname', alias.confidence = 'high',
//     alias.analyst_notes = 'Common nickname for William',
//     alias.created_date = datetime()
// MERGE (p)-[:KNOWN_AS]->(alias);

// MATCH (p:Person {name: '@Hawk, Kenzie'})
// MERGE (alias:Alias {rawValue: 'Ken', canonical: p.name})
// SET alias.type = 'abbreviation', alias.confidence = 'medium',
//     alias.analyst_notes = 'Possible abbreviation used in communications',
//     alias.created_date = datetime()
// MERGE (p)-[:KNOWN_AS]->(alias);