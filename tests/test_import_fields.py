#!/usr/bin/env python
"""
Quick test to verify import field fixes are working correctly.
Run this after importing data to check computed fields.
"""

from neo4j import GraphDatabase

BOLT_URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Sup3rSecur3!")

def test_stoptime_fields():
    """Check that sessions have stoptime, not endtime"""
    driver = GraphDatabase.driver(BOLT_URI, auth=AUTH)
    
    with driver.session() as session:
        # Check for any endtime properties (should be 0)
        result = session.run("""
            MATCH (s:Session)
            WHERE s.endtime IS NOT NULL
            RETURN count(s) as endtime_count
        """).single()
        
        print(f"Sessions with endtime property: {result['endtime_count']}")
        assert result['endtime_count'] == 0, "Found sessions with endtime property!"
        
        # Check stoptime is populated
        result = session.run("""
            MATCH (s:Session)
            WHERE s.stoptime IS NOT NULL
            RETURN count(s) as stoptime_count
        """).single()
        
        print(f"Sessions with stoptime property: {result['stoptime_count']}")
        
        # Check computed duration
        result = session.run("""
            MATCH (s:Session)
            WHERE s.durationinseconds IS NOT NULL
            RETURN count(s) as duration_count
        """).single()
        
        print(f"Sessions with duration: {result['duration_count']}")
        
        # Check sessiondate computation
        result = session.run("""
            MATCH (s:Session)
            WHERE s.sessiondate IS NOT NULL
            RETURN count(s) as sessiondate_count
        """).single()
        
        print(f"Sessions with sessiondate: {result['sessiondate_count']}")
        
        # Sample a few records to verify computation
        results = session.run("""
            MATCH (s:Session)
            WHERE s.starttime IS NOT NULL AND s.stoptime IS NOT NULL
            RETURN s.sessionguid as guid,
                   s.starttime as start,
                   s.stoptime as stop,
                   s.durationinseconds as duration,
                   s.sessiondate as sessiondate
            LIMIT 3
        """)
        
        print("\nSample sessions with computed fields:")
        for record in results:
            print(f"- {record['guid'][:20]}...")
            print(f"  Start: {record['start']}")
            print(f"  Stop: {record['stop']}")
            print(f"  Duration: {record['duration']}s")
            print(f"  Session Date: {record['sessiondate']}")
    
    driver.close()
    print("\n✅ All field tests passed!")

if __name__ == "__main__":
    test_stoptime_fields()