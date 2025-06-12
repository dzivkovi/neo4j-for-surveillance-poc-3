// =============================================================================
// PRACTICAL INVESTIGATION QUERIES FOR LAW ENFORCEMENT
// =============================================================================
// These queries focus on real investigative value rather than visual impressiveness

// =============================================================================
// 1. COMMUNICATION FREQUENCY ANALYSIS
// =============================================================================
// Find the most active communication pairs (potential conspirators)
MATCH (p1:Person)-[:USES]->(acc1)-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(acc2)<-[:USES]-(p2:Person)
WHERE p1 <> p2
WITH p1.name as person1, p2.name as person2, count(DISTINCT s) as total_sessions,
     collect(DISTINCT s.sessiontype) as communication_types,
     min(s.starttime) as first_contact,
     max(s.starttime) as last_contact
WHERE total_sessions >= 5
RETURN person1, person2, total_sessions, communication_types, first_contact, last_contact
ORDER BY total_sessions DESC;

// =============================================================================
// 2. DEVICE SHARING INVESTIGATION
// =============================================================================
// Find all people who have used the same devices (operational security breach)
MATCH (p1:Person)-[:USES_DEVICE]->(d:Device)<-[:USES_DEVICE]-(p2:Person)
WHERE p1 <> p2
WITH d.imei as device_id, collect(DISTINCT p1.name) + collect(DISTINCT p2.name) as users
RETURN device_id, users, size(users) as user_count
ORDER BY user_count DESC;

// =============================================================================
// 3. BURNER PHONE DETECTION
// =============================================================================
// Find phones used for very few sessions (potential burner phones)
MATCH (ph:Phone)-[:PARTICIPATED_IN]->(s:Session)
WITH ph.number as phone_number, count(DISTINCT s) as session_count,
     collect(DISTINCT s.sessiontype) as session_types,
     min(s.starttime) as first_use,
     max(s.starttime) as last_use
WHERE session_count <= 5
RETURN phone_number, session_count, session_types, first_use, last_use,
       duration.between(datetime(first_use), datetime(last_use)).days as days_active
ORDER BY session_count ASC;

// =============================================================================
// 4. NIGHT OWL ANALYSIS
// =============================================================================
// Find people who primarily communicate during suspicious hours (11 PM - 5 AM)
MATCH (p:Person)-[:USES]->(acc)-[:PARTICIPATED_IN]->(s:Session)
WHERE s.starttime IS NOT NULL
WITH p, s, time(s.starttime).hour as hour
WHERE hour >= 23 OR hour <= 5
WITH p.name as person, count(DISTINCT s) as night_sessions
MATCH (p2:Person {name: person})-[:USES]->(acc2)-[:PARTICIPATED_IN]->(s2:Session)
WITH person, night_sessions, count(DISTINCT s2) as total_sessions,
     round(100.0 * night_sessions / count(DISTINCT s2), 1) as night_percentage
WHERE night_percentage > 30
RETURN person, night_sessions, total_sessions, night_percentage
ORDER BY night_percentage DESC;

// =============================================================================
// 5. COMMUNICATION HUB IDENTIFICATION
// =============================================================================
// Find people who act as bridges between different groups
MATCH (hub:Person)-[:USES]->(acc1)-[:PARTICIPATED_IN]->(s1:Session)<-[:PARTICIPATED_IN]-(acc2)<-[:USES]-(contact:Person)
WHERE hub <> contact
WITH hub.name as hub_person, count(DISTINCT contact) as unique_contacts,
     count(DISTINCT s1) as total_sessions
WHERE unique_contacts >= 10
RETURN hub_person, unique_contacts, total_sessions,
       round(1.0 * total_sessions / unique_contacts, 1) as avg_sessions_per_contact
ORDER BY unique_contacts DESC;

// =============================================================================
// 6. ENCRYPTED COMMUNICATION DETECTION
// =============================================================================
// Find sessions with encrypted or encoded content
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE c.text =~ '.*([A-Za-z0-9+/]{20,}|BEGIN PGP|-----BEGIN|[0-9a-fA-F]{32,}).*'
   OR c.text =~ '.*(encrypted|cipher|key|password).*'
RETURN s.sessionguid, s.sessiontype, s.targetname, 
       substring(c.text, 0, 200) as content_preview
LIMIT 20;

// =============================================================================
// 7. MULTI-DEVICE USER ANALYSIS
// =============================================================================
// Find people using multiple devices (operational security awareness)
MATCH (p:Person)-[:USES_DEVICE]->(d:Device)
WITH p.name as person, collect(d.imei) as devices, count(d) as device_count
WHERE device_count > 1
MATCH (p2:Person {name: person})-[:USES_DEVICE]->(d2:Device)-[:HAS_ACCOUNT]->(ph:Phone)
WITH person, devices, device_count, collect(DISTINCT ph.number) as phone_numbers
RETURN person, device_count, devices, phone_numbers
ORDER BY device_count DESC;

// =============================================================================
// 8. CALL DURATION ANOMALIES
// =============================================================================
// Find unusually long calls (Telephony sessions longer than 2 minutes)
MATCH (s:Session)
WHERE s.sessiontype = 'Telephony' AND s.durationinseconds IS NOT NULL
WITH s, s.durationinseconds as duration_seconds
WHERE duration_seconds > 120  // Calls longer than 2 minutes
MATCH (s)<-[:PARTICIPATED_IN]-(ph:Phone)<-[:USES]-(p:Person)
WITH s.sessionguid as sessionguid, s.targetname as targetname, 
     duration_seconds as duration_seconds,
     s.starttime as starttime, collect(DISTINCT p.name) as participants
RETURN sessionguid, targetname, duration_seconds, starttime, participants
ORDER BY duration_seconds DESC;

// =============================================================================
// 9. COMMUNICATION PATTERN CHANGES
// =============================================================================
// Detect sudden changes in communication patterns (before/after a date)
WITH datetime('2022-06-15T00:00:00') as cutoff_date
MATCH (p:Person)-[:USES]->(acc)-[:PARTICIPATED_IN]->(s:Session)
WHERE s.starttime IS NOT NULL
WITH p, s, cutoff_date,
     CASE WHEN datetime(s.starttime) < cutoff_date THEN 'before' ELSE 'after' END as period
WITH p.name as person, period, count(DISTINCT s) as session_count
WITH person, 
     sum(CASE WHEN period = 'before' THEN session_count ELSE 0 END) as before_count,
     sum(CASE WHEN period = 'after' THEN session_count ELSE 0 END) as after_count
WHERE before_count > 0 AND after_count > 0
RETURN person, before_count, after_count,
       round(100.0 * (after_count - before_count) / before_count, 1) as percent_change
ORDER BY abs(percent_change) DESC;

// =============================================================================
// 10. FIND SHORTEST PATH BETWEEN SUSPECTS
// =============================================================================
// Find how two people are connected through the network
// Replace the names with your persons of interest
MATCH path = shortestPath(
  (p1:Person {name: 'Eagle, Richard'})-[*]-(p2:Person {name: 'Hawk, Kenzie'})
)
RETURN path,
       [node in nodes(path) WHERE node:Person | node.name] as people_in_path,
       length(path) as degrees_of_separation;

// =============================================================================
// 11. GROUP DETECTION VIA COMMON SESSIONS
// =============================================================================
// Find groups of 3+ people who frequently communicate together
MATCH (s:Session)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
WITH s, collect(DISTINCT p.name) as participants
WHERE size(participants) >= 3
RETURN participants, count(s) as multi_party_sessions
ORDER BY multi_party_sessions DESC;

// =============================================================================
// 12. CONTENT KEYWORD SEARCH
// =============================================================================
// Search for specific keywords in communications
// Modify the keywords list as needed
WITH ['money', 'payment', 'transfer', 'cash', 'bitcoin', 'meet', 'location'] as keywords
MATCH (s:Session)-[:HAS_CONTENT]->(c:Content)
WHERE any(keyword IN keywords WHERE toLower(c.text) CONTAINS keyword)
WITH s, c, [keyword IN keywords WHERE toLower(c.text) CONTAINS keyword] as found_keywords
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
RETURN s.sessionguid, s.sessiontype, collect(DISTINCT p.name) as participants,
       found_keywords, substring(c.text, 0, 200) as content_preview
LIMIT 20;

// =============================================================================
// 13. LONGEST SESSIONS BY TYPE
// =============================================================================
// Find the longest sessions of each type - useful for identifying important events
MATCH (s:Session)
WHERE s.durationinseconds IS NOT NULL AND s.durationinseconds > 0
MATCH (s)<-[:PARTICIPATED_IN]-(acc)<-[:USES]-(p:Person)
WITH s.sessiontype as session_type, s.sessionguid as session_id, s.targetname as target,
     s.durationinseconds as duration, s.starttime as start_time,
     collect(DISTINCT p.name) as participants
RETURN session_type, session_id, target, duration, start_time, participants
ORDER BY duration DESC
LIMIT 20;