// quick counts to verify import
MATCH (s:Session) RETURN 'Sessions' AS label, count(*) AS n
UNION ALL
MATCH (p:Person)  RETURN 'Persons' AS label, count(*) AS n
UNION ALL
MATCH (p:Phone)   RETURN 'Phones' AS label, count(*) AS n
UNION ALL
MATCH (d:Device)  RETURN 'Devices' AS label, count(*) AS n
UNION ALL
MATCH (e:Email)   RETURN 'Emails' AS label, count(*) AS n
UNION ALL
MATCH (c:Content) RETURN 'Content' AS label, count(*) AS n;
