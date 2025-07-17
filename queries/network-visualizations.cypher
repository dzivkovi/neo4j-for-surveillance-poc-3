// =============================================================================
// NETWORK VISUALIZATION QUERIES FOR SURVEILLANCE ANALYTICS
// =============================================================================
// Curated queries that produce meaningful connected graph visualizations
// Best viewed in Neo4j Browser's Graph mode

// =============================================================================
// 1. CORE COMMUNICATION NETWORK
// =============================================================================
// Shows the primary communication paths between active participants
// Returns full paths to ensure connections are displayed
MATCH path = (p1:Person)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p2:Person)
WHERE p1 <> p2
WITH p1, p2, count(DISTINCT s) as strength
WHERE strength >= 3
MATCH path = (p1)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p2)
RETURN path
LIMIT 50;

// =============================================================================
// 2. DEVICE SHARING CONSTELLATION
// =============================================================================
// Visualizes device sharing patterns - critical for operational security analysis
MATCH path = (p1:Person)-[:USES_DEVICE]->(d:Device)<-[:USES_DEVICE]-(p2:Person)
WHERE p1 <> p2
WITH path, d
MATCH device_sessions = (d)-[:HAS_ACCOUNT]->(phone:Phone)-[:PARTICIPATED_IN]->(s:Session)
RETURN path, device_sessions
LIMIT 30;

// =============================================================================
// 3. HUB-AND-SPOKE ANALYSIS
// =============================================================================
// Centers on the most connected individuals to show their networks
// Replace '@Kenzie Hawk' with any person of interest
// Top hubs: @Kenzie Hawk (16 contacts), @Eagle, Richard (11 contacts), @Hawk, Kenzie (9 contacts)
MATCH (hub:Person {name: '@Kenzie Hawk'})
MATCH path = (hub)-[:USES]->()-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(contact:Person)
WHERE hub <> contact
RETURN hub, path
LIMIT 25;

// =============================================================================
// 4. SESSION-CENTRIC VIEW
// =============================================================================
// Shows sessions with multiple participants - useful for group detection
MATCH (s:Session)
WHERE s.durationinseconds > 300  // Sessions longer than 5 minutes
MATCH path = (s)<-[:PARTICIPATED_IN]-(participant)
WITH s, collect(path) as paths, count(DISTINCT participant) as participant_count
WHERE participant_count >= 2
UNWIND paths as path
RETURN s, path
LIMIT 40;

// =============================================================================
// 5. COMMUNICATION CHAINS
// =============================================================================
// Shows how information might flow through the network
MATCH chain = (p1:Person)-[:USES]->()-[:PARTICIPATED_IN]->(:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-
              (p2:Person)-[:USES]->()-[:PARTICIPATED_IN]->(:Session)<-[:PARTICIPATED_IN]-()<-[:USES]-(p3:Person)
WHERE p1 <> p2 AND p2 <> p3 AND p1 <> p3
RETURN chain
LIMIT 20;

// =============================================================================
// 6. MULTI-HOP INVESTIGATION
// =============================================================================
// Explore network connections up to 3 hops from a person of interest
// Adjust the person name and hop count as needed
MATCH (poi:Person {name: '@Eagle, Richard'})
MATCH path = (poi)-[:USES|USES_DEVICE|PARTICIPATED_IN*1..6]-(connected)
WHERE connected:Person AND connected <> poi
RETURN path
LIMIT 30;

// =============================================================================
// 7. TEMPORAL ACTIVITY BURST
// =============================================================================
// Shows concentrated communication activity on specific dates
// Useful for identifying coordinated operations
MATCH (s:Session)
WHERE date(s.starttime) = date('2022-06-22')  // Adjust date as needed
MATCH path = (s)<-[:PARTICIPATED_IN]-(part)<-[:USES]-(p:Person)
RETURN s, path
LIMIT 50;

// =============================================================================
// 8. COMPLETE SUBGRAPH EXTRACTION
// =============================================================================
// Returns a complete connected component with all relationships
// Good for detailed analysis of a specific group
MATCH (p1:Person)-[r1:USES]->(acc1)-[r2:PARTICIPATED_IN]->(s:Session)<-[r3:PARTICIPATED_IN]-(acc2)<-[r4:USES]-(p2:Person)
WHERE p1.name IN ['@Eagle, Richard', '@Eagle, William', '@Merlin, Fred']
  AND p2.name IN ['@Eagle, Richard', '@Eagle, William', '@Merlin, Fred']
  AND p1 <> p2
RETURN p1, r1, acc1, r2, s, r3, acc2, r4, p2
LIMIT 30;

// =============================================================================
// VISUALIZATION TIPS:
// =============================================================================
// 1. Always use "Graph" view in Neo4j Browser (not Table/Text)
// 2. After running a query:
//    - Drag nodes apart to see connections clearly
//    - Double-click nodes to expand relationships
//    - Use Ctrl+Click to select multiple nodes
// 3. Styling:
//    - Click the style button (bottom right)
//    - Color nodes by label or property
//    - Size nodes by degree or property
// 4. Browser Settings:
//    - Initial Node Display: 300
//    - Max Neighbours: 100
//    - Connect result nodes: ON