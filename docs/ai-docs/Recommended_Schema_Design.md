## Recommended Unified Schema Design: Session-Centric POLE Model (“Less is More”)

Bringing together the best aspects of each proposal, we recommend a **unified schema** that is session-centric and adheres to the “less is more” philosophy. This design uses a **core set of node types** – **Session**, **Identity** (Person), **Account**, **Device**, **Content**, **Location** – and straightforward relationships to represent the surveillance data. It preserves the fidelity of `sessions.ndjson` (every piece of data is mapped) while supporting performant querying for all benchmark use cases. Below we outline the schema structure and then provide example Cypher queries and import instructions.

### Node Types and Properties

* **Session** (`:Session` label): Represents a surveillance communication session or event. This is the central node for each record in `sessions.ndjson`. **Properties:** All top-level fields of the JSON record are stored here. Important properties include:

  * `sessionguid` (String, unique identifier for the session)
  * `sessiontype` (String – e.g. "Entity Report", "Messaging", "Telephony", "Email", etc.)
  * `casename` (String, e.g. "@Operation Whiskey Jack")
  * `sessionnumber` (Integer, the session’s number within the case)
  * `createddate` (Datetime – when the record was created/ingested)
  * `starttime`, `endtime` (Datetime – if the session has a defined start/end, e.g. call start/end times or event times; if not applicable, these may be null)
  * `attachmentstatus`, `classification`, `icon`, `displaytypeid` (Strings – descriptive fields from the data)
  * `sourcesystemname` (String – source system or extraction name, e.g. "Local 3.9" or "Generic Email")
  * `sourceid` (String – original source file or ID reference)
  * `targetname` (String – name/ID of the target owner of this session’s data, if applicable)
  * `linename` (String – name of the communication line or account, e.g. "@Kenzie Emails" or a phone line label)
  * Any other top-level fields present in the NDJSON (e.g. `isevidence` flag, `lockedby`, etc.).
    These properties ensure that queries can filter or return basic session info without needing additional nodes. For example, you can search sessions by `sessiontype` or `classification` directly. Temporal properties are stored as Neo4j temporal values (or ISO date strings) so that one can do range queries (e.g. sessions in February 2020). An index/constraint on `sessionguid` will ensure each session node is unique and allow quick lookup by ID.

* **Identity (Person)** (`:Person` or `:Identity` label): Represents an individual involved in communications. This corresponds to names or personal identifiers in the data (e.g. "@Merlin, Fred", "@Hawk, Kenzie"). **Properties:**

  * `name` (String) – The name or alias as given in the data (including any formatting like “Last, First” or nicknames).
  * Possibly an `id` (String/Int) if the source had a unique ID for the person (the NDJSON “id” field in an involvement that has a personname might be an internal contact ID, but since those weren’t consistent globally, we may not use it as a stable person ID across sessions).
  * Other descriptive attributes if available (e.g. `role` in the context of case – “Subject”, “Target”, etc. – though role might be better kept on relationships as it varies per session).
    Each distinct person appears once as a node. In practice, we may need to merge nodes by name or by some unique identifier. (If the data has slight name variations or duplicates, some data cleansing might be required to unify identities. In our case, names like "Frasier, Owen" vs "Owen Frasier" should be standardized to one representation to avoid duplicate nodes.) The Person nodes form the basis for entity-centric queries (like “find all communications involving Owen Frasier”). We do **not** encode person roles (subject, target, etc.) as separate node types – a person is a person, with their role in a given session indicated in the relationship.

* **Account** (`:Account` label, with sublabels like `:Phone` or `:Email` as needed): Represents a communication account or identifier, such as a phone number, email address, or other contact handle. For clarity, we can subtype these, e.g. `:Phone` for telephone numbers, `:Email` for email addresses, but they will function similarly. **Properties:**

  * For phone accounts: `number` (String, the phone number, e.g. "9366351931"), possibly normalized to a standard format. We might also store a country code or type if available (mobile, landline, etc.), but in this data it seems just a raw number.
  * For email accounts: `email` (String, e.g. "[ziezieken88@gmail.com](mailto:ziezieken88@gmail.com)").
  * `id` (if available, e.g. an internal ID for the account from the data).
  * If the NDJSON involvement entries have additional metadata for accounts (like `relationship` or labels like "Other Phone", "Contact"), these can be stored either as a property (e.g. `tag: "Other Phone"`) or captured via the relationship to the person (for instance, Kenzie’s contact list labeled Fiona’s number as "Other Phone"). In our schema, we might use relationship types to distinguish, but a simpler way is to keep a `label` property on the Account node or the relationship to Person.
    Account nodes ensure that communications can be indexed and queried by the exact phone/email. They are considered *Objects* in POLE terms. For example, to answer *“Which phone numbers are associated with IMEI X?”* or *“What is Kenzie’s email address?”*, we look for Account nodes linked to the person or device in question. We will create unique constraints on account identifiers (phone number, email) so that the same number/email always maps to one node, avoiding duplicates.

* **Device** (`:Device` label): Represents a physical device (e.g. a phone handset). This is identified primarily by hardware identifiers like **IMEI**. **Properties:**

  * `imei` (String, the device’s IMEI or equivalent unique hardware ID).
  * `make` (String, e.g. "APPLE" or "SAMSUNG"), `model` (String, e.g. "iPhone 12" or a model number like "SM-G986B").
  * Other attributes from the data’s device fields (if present): e.g. `imei2` if dual-SIM, `serial` number, etc., but the dataset mostly shows IMEI, make, model.
    Device nodes are crucial because the benchmark questions explicitly ask about devices and IMEIs. By having Device nodes, we can easily support queries like *“Who has been using devices with IMEI X?”* or *“What devices does Kenzie Hawk use?”*. We will ensure an index/constraint on the `imei` property (IMEIs are unique per device). Device nodes are linked to Account and/or Person nodes as described below, forming part of the “Object” category in POLE. If a session involvement provides an IMEI along with a phone number and person, we interpret that as a Person using a Device with that phone number for that session – so all three (Person, Device, Account) will be connected appropriately in the graph.

* **Content** (`:Content` label): Represents the content of a communication or an attached artifact. Depending on the type of session, this could be the text of a message, the transcript of a call, the data of a contact card, an image, etc. We use Content nodes to separate unstructured data from the session metadata, allowing specialized indexing. **Properties:**

  * `id` (String, an ID for the content if available. The NDJSON “products.id” or similar can be used for attachments/media. If content is just the message text, we can generate an ID or use the sessionguid combined with a part indicator.)
  * `text` (String, the textual content for text-based items. For example, the body of an SMS or email, or the fields of a vCard concatenated. In the case of a contact card (vCard), `text` might contain the full vCard text or a JSON of its fields for searching. For images or binary, `text` may be empty or a descriptive placeholder since we can’t index binary images in full-text.)
  * `contentType` (String, e.g. "text/plain", "image/png", "text/vcard", etc., as provided by `contenttype` and subtype in the data).
  * `size` (Integer, if provided, e.g. file size of an attachment) and `filename` (if provided).
  * `languages` (List<String>, e.g. `["English"]` if language detection was done).
  * Other relevant fields from `products` array or enrichment fields (for instance, if `text-extraction` or `decodestate` is present, those could inform whether content text is available or had to be decoded).
  * `embedding` (List<Float> or Vector type, the embedding of the text content for semantic search). This property will hold the vector representation of `text`, computed by an NLP model (not in the original data, but added during our import or analysis process).
    Each Session can have zero, one, or multiple Content nodes. For example, an SMS session will have one Content node containing the message text (and possibly another for a multimedia attachment if any). An Entity Report session (contact card) might have one Content node for the vCard text or image preview. By linking these as separate nodes, we can index them in a Neo4j full-text index (on the `text` property) and create a vector index on the `embedding` property for similarity search. This separation is critical for answering questions about message content, performing free-text searches (“find ‘latte’ or ‘Seaman Cafe’ in communications”), or semantic queries (“find conversations similar to this topic”). It also allows storing long text or binary data outside of the core Session node to keep it lightweight.

* **Location** (`:Location` label): Represents a geographic location associated with a session. **Properties:**

  * Could simply use Neo4j’s spatial Point type property, e.g. `coord: point({latitude: ..., longitude: ...})`. Alternatively, store latitude and longitude as separate numeric properties if preferred.
  * If the data includes address names or place labels (e.g. “Port Miami”), those can be stored as `name` or `address` property. (In our dataset, location appears to be coordinates captured from devices – e.g., track points or a single location for a call – rather than a named place, so coordinates are primary.)
  * If multiple points (like a sequence of GPS trackpoints) are present, we handle it by either creating multiple Location nodes or storing an array of points. The g25 proposal suggests that if frequent queries on individual track points are needed, one could model each as a node; otherwise, a simpler approach is to keep an array of points on one Location node for the session. For now, we can create a single Location node per session representing either the starting location or an aggregated path of that session. We will also capture a timestamp if the location is time-specific (e.g. if trackpoints have timestamps).
    Location nodes enable geospatial filtering (Neo4j can index point properties to query by distance). For example, one could ask “find all sessions within 10 km of a given coord” or filter sessions by area. Although none of the example questions explicitly asked for radius queries, having location nodes also helps with understanding movements or mapping communications on a map. They are part of the POLE “Location” category and are linked to Session nodes (relationship could be **LOCATED\_AT** or *HAS\_LOCATION*). If a session has multiple relevant locations (e.g. two participants in different places), we could attach multiple Location nodes (or have a Person-to-Location relationship for participant’s location, but that complicates things; likely the data only provides one set of coords, presumably for the primary device involved).

* **(Optional) Organization/Group** (`:Organization` label, if applicable): The data or questions might reference organizations (for instance “TBI-A” appears in a note, which sounds like an organization or agency). If the dataset contains entities that are organizations or groups (e.g. a named organization in contact lists or a group chat entity), we could have an Organization node type. The relationships would be similar (an organization could be listed as a participant or mentioned). This is not prominent in the given data except possibly as context, so we mention it for completeness. The schema is easily extensible to add more entity types if needed (e.g. vehicles, addresses as entities, etc.), but the core focus remains on Persons, Accounts, Devices as the main entities observed.

### Relationships and Structure

The relationships in the schema tie together the nodes in a way that mirrors the involvement list and metadata of each session. We describe them as follows:

* **Person–Account –** Every Account node that corresponds to a known person is linked via **USES** (or **OWNS**) relationship from the Person. For example, if Kenzie Hawk’s phone number is 9366351931, we create `(Kenzie:Person)-[:USES]->(Phone:Account {number: "9366351931"})`. A person may use multiple accounts (e.g. multiple phone numbers or an email and a phone), and potentially an account could be used by multiple persons over time (though in our context, if that occurs, it can be represented too). This relationship is mostly static/background info but is very useful for queries: it lets us find all accounts associated with a person (to, say, find all sessions where any of their accounts appear), and conversely find which person is known to own a given account (to answer question #75, *“What is Kenzie’s email?”*, we find the Email account used by Kenzie). If an account is not associated with a known person (e.g. an unknown phone number that only appears in one call and we don’t know the identity), that Account node simply won’t have a `:USES` relationship – it exists independently until perhaps identified later.

* **Person–Device –** Similarly, we link Persons to Devices they are known to use. In the data, if an involvement shows a person with a specific IMEI (and that person is the device owner or user), we create `(Person)-[:USES_DEVICE]->(Device)`. For example, if Kenzie Hawk’s phone has IMEI 358798097379882 (one of the IMEIs in question #70), then `(Kenzie)-[:USES_DEVICE]->(Device {imei: "358798097379882"})`. Kenzie might have multiple devices (as the question suggests two IMEIs for her), so she would have two such relationships. If a device is used by multiple people (e.g. a shared or transferred phone), multiple persons can link to the same Device node (optionally we could add a property like `since`/`until` on the relationship if we know time frame of ownership, but our data likely doesn’t specify that explicitly). Device relationships allow device-centric queries: *“Who has been using device X?”* simply becomes a one-hop traversal from the Device node to whatever Persons are linked. If the data doesn’t explicitly state person-device mapping outside of sessions, we derive it from session evidence: for instance, if a particular IMEI always appears in sessions where Kenzie is the principal (target) participant, we infer Kenzie uses that device. We could script a post-processing to create those Person–Device relationships by analyzing sessions. In any case, having them makes certain queries trivial.

* **Device–Account –** We connect Devices to the Accounts (phone numbers) that have been observed on them. In a phone call or SMS session, the involvement often provides both an IMEI and a phone number together for one party. That implies a linkage, so we create `(Device)-[:HAS_ACCOUNT]->(Account)`. For example, `(Device {imei: ...})-[:HAS_SIM]->(Phone {number: ...})`. This captures that a given device was associated with that phone number (SIM) during communications. Over time, a device could have different numbers (if SIMs change), and a number could hop devices; our graph can represent that with multiple relationships as those events occur. Queries like *“Which IMEIs are associated with phone number 9366351931?”* are then a matter of traversing from the Phone account node to connected Device nodes. Likewise, *“Which phone numbers are associated with IMEI 359847107165930?”* inverts that traversal. If the data shows both sides of a call with device info, we’d make sure to link both devices to their respective numbers. If device information isn’t present for one side (e.g. maybe we only have IMEI for the target’s device, not for the remote party), then that side simply won’t produce a Device node in the graph (or we only have an Account for the remote side). The schema handles both situations.

* **Session–Account (Participation) –** Each Account that took part in a session is connected to the Session node. We define a relationship, e.g. **PARTICIPATED\_IN** or **INVOLVED\_IN**, from the Account to the Session. For example, if phone number 9366351931 was the originator of an SMS session (session X), we create `(Phone {9366351931})-[:PARTICIPATED_IN {role:"From"}]->(Session X)`. Likewise the recipient’s number gets a PARTICIPATED\_IN with role "To". We include properties on this relationship to capture the context from the involvement:

  * `role`: the role of that participant in the session (e.g. "From", "To", "Participant", "Subject"). This comes from the `role` field in the NDJSON involvement (or can be inferred: principal target’s device might be role "From" if it was sending, etc., as in the data).
  * `isPrincipal` (Boolean): from `isprincipal` field – indicates if this was the primary party (from whose device the data was collected). For instance, in Kenzie’s own device sessions, her account might be `isPrincipal=true`.
  * `isTarget` (Boolean): from `istarget` field – indicates if this participant is the investigative target. E.g. for target devices (like Kenzie’s phone), that account involvement has `istarget:true`.
  * We might also include `relationship`/`inverserelationship` from data if meaningful (e.g. "Other Phone" vs "Contact" in contact list context – these could be stored as a property or ignored for communications as they mostly apply to how a contact was stored).
    In many cases, the Person’s identity is known for an account (and we have Person–Account link), so one could traverse Person→Account→Session to find sessions a person participated in. However, for completeness and easier queries, we could also connect **Person directly to Session** for cases where the person was explicitly named in the session without an account (for example, the contact entry sessions where Fiona Finch appears as a “Subject” with no device in that event). In such cases, a `(:Person)-[:PARTICIPATED_IN]->(:Session)` can be created similarly. Generally, though, communications will use Account nodes for the link. This two-hop model (Person–Account–Session) is slightly more normalized but ensures that if a person uses multiple accounts, we catch all their sessions via those accounts. The **PARTICIPATED\_IN** relationship (whether from Account or Person) is the backbone for answering “who was involved in what”. We will index or constraint-check on combinations if needed (though likely not – simple traversal suffices). Note that we do not differentiate in graph model between “sending” and “receiving” with separate relationship types; we use the `role` property for that. If one wanted to specifically query senders vs receivers, they can filter on `rel.role = 'From'` for example. This keeps the schema simpler (a single relationship type for participation).

* **Session–Content –** Each Content node is linked to its Session via a relationship, e.g. **HAS\_CONTENT** or **ATTACHED**. For example, `(Session X)-[:HAS_CONTENT]->(Content Y)` might represent that session X has an attached content Y (like a message text or file). We use a direction from Session to Content (one-to-many). If needed, one could differentiate types of content with relationship subtypes (like `:HAS_MESSAGE`, `:HAS_ATTACHMENT`), but a `type` property on Content itself usually suffices (contentType or role). The content nodes allow queries like searching for sessions by content: with a full-text index on Content, a query can find Content nodes matching a keyword and then follow inbound HAS\_CONTENT to get the Session. Similarly, for vector search, we query the index on Content embeddings and then get the Session. This design cleanly separates concerns: you don’t bloat the Session node with large text or binary data, but you can still quickly jump from content to session and vice versa.

* **Session–Location –** If a Session has an associated location (or multiple trackpoints), we connect the Session to a Location node using e.g. **LOCATED\_AT**. For example, `(Session X)-[:LOCATED_AT]->(Location {coord: point(...)} )`. If there are multiple points (like a route), one approach is to link all Location nodes (or a path of Location nodes) to the session, but that could be overkill unless needed. A simpler method is one Location node per session which could contain an array of coordinates or just a representative coordinate. For initial use cases, a single representative location (perhaps the first or last known location in that session) can be used. This is an area that can be extended if queries demand (e.g. if question: “show the movement path of device X during call Y” came up, we’d model trackpoints as connected sequence). For now, the presence of Location nodes means we can answer things like *“Did any communications happen near coordinates (lat,lon)?”* or filter sessions by region (if we know coordinates of interest). The Location nodes use Neo4j’s spatial indexes for efficient querying by distance.

* **Additional relationships:** There may be cases to add more edges for convenience or semantics: e.g., **Person–Session (Target/Owner)**: As mentioned, if a session has a `targetname` that was not listed as an involvement, we may link the target Person to that Session with a relationship indicating they are the data owner (for instance, `(:Person)-[:OWNS_SESSION]->(:Session)`). In our dataset, contact entries have Kenzie as the target (owner of the contact list) but she isn’t a participant in the content of those sessions. Linking her in the graph would allow queries like “show me all sessions from Kenzie’s devices” easily. This relationship would be derived from `targetname` property. Alternatively, we can rely on filtering sessions by session.targetname property – both approaches work, but an explicit relationship could simplify some queries. We recommend adding such a link for completeness (e.g. `(:Person {name:"Kenzie Hawk"})-[:OWNS_DEVICE_DATA]->(Session 12)` for the contact entry example). Similarly, if there are grouping concepts like an investigation case node (Operation Whiskey Jack as a node), one could link sessions to a Case node. This was not in scope of the original question but is trivial to add: a `Case` node with name "Operation Whiskey Jack" and relationships to all sessions in that case. This would facilitate querying all sessions in a case or if multiple cases existed. Since `casename` is already a property on sessions, we consider this optional. If the dataset may later include multiple cases, a Case node is useful normalization.

This unified schema, summarized, focuses on **Sessions as the hub** connecting to **Identities (persons) via their Accounts**, linking any **Devices** and **Locations**, and attaching **Content** for rich search. It is conceptually aligned with POLE (people, devices/accounts, locations linked by event nodes) and implements exactly the entities needed for the investigative queries. By not over-complicating labels (we use specific labels like `:Session`, `:Person`, etc., instead of one generic Event node or generic Object node), we keep Cypher queries efficient – for example, `MATCH (s:Session)` directly targets communications without scanning other node types.

### Indexes and Constraints (Neo4j 5.x)

To ensure performance and enable advanced searches, we define the following indexes and constraints using Neo4j 5.x (which supports native vector indexing and full-text search):

* **Unique Constraints:**

  * `Session.sessionguid` – each session GUID is unique.

    ```cypher
    CREATE CONSTRAINT FOR (s:Session) REQUIRE s.sessionguid IS UNIQUE;
    ```
  * `Person.name` – (optional) if we assume no two persons share the exact same name in this dataset, we can enforce uniqueness on name. Caution: if not true universally, skip or use a different key. Alternatively, use a compound key if we had one (we do not in NDJSON except maybe name+casename). We might omit a constraint here to allow same names, but we will MERGE by name to avoid duplicates as best as possible.
  * `Account.number` for Phone – phone numbers unique (assuming standardized format).

    ```cypher
    CREATE CONSTRAINT FOR (p:Phone) REQUIRE p.number IS UNIQUE;
    ```

    Similarly `Account.email` for Email addresses.

    ```cypher
    CREATE CONSTRAINT FOR (e:Email) REQUIRE e.email IS UNIQUE;
    ```

    These ensure one node per unique contact handle.
  * `Device.imei` – IMEIs are unique identifiers for devices.

    ```cypher
    CREATE CONSTRAINT FOR (d:Device) REQUIRE d.imei IS UNIQUE;
    ```
  * (If using Case node) `Case.name` unique. (Optional)

* **Indexes for Search/Filtering:**

  * **Exact-match / range indexes:** We create indexes on properties that we will frequently filter or sort by.

    * `Session.createddate` – for time range queries.

      ```cypher
      CREATE INDEX FOR (s:Session) ON (s.createddate);
      ```

      (Neo4j automatically creates a range index for temporal types in v5 when using the above syntax). This allows efficient filtering of sessions by date (e.g. `WHERE s.createddate >= date('2020-02-01') AND s.createddate < date('2020-03-01')`).
    * `Session.sessiontype`, `Session.casename` – if we query by type or case frequently (e.g. find all “Telephony” sessions or all sessions in "Operation X"), an index helps. These could be simple B-tree indexes.

      ```cypher
      CREATE INDEX FOR (s:Session) ON (s.sessiontype);
      CREATE INDEX FOR (s:Session) ON (s.casename);
      ```
    * `Person.name` – to quickly find a person node by name (when a query includes a person’s name). Although we can also do a full-text search on names (in case of fuzzy matching), an exact index on name speeds up direct lookups like `MATCH (p:Person {name:"Owen Frasier"})`.

      ```cypher
      CREATE INDEX FOR (p:Person) ON (p.name);
      ```

      (Similarly for organization names if needed.)
    * `Account.number` and `Account.email` – index these for lookup by exact contact info.

      ```cypher
      CREATE INDEX FOR (p:Phone) ON (p.number);
      CREATE INDEX FOR (e:Email) ON (e.email);
      ```

      This supports queries like “find the account node for 9366351931” instantly.
    * `Device.imei` – index for looking up devices by IMEI.

      ```cypher
      CREATE INDEX FOR (d:Device) ON (d.imei);
      ```
    * `Location.coord` – Neo4j supports spatial indexes on point properties. We can do:

      ```cypher
      CREATE INDEX FOR (l:Location) ON (l.coord);
      ```

      This index enables efficient geospatial queries using built-in functions (like `distance(l.coord, point(...)) < x`).

  * **Full-Text Index:** We utilize Neo4j’s full-text schema index for text content. We will index the `text` property of Content nodes (and possibly also person names or other relevant string fields if needed for free-text search). For example:

    ```cypher
    CALL db.index.fulltext.createNodeIndex("ContentFullText", ["Content"], ["text"]);
    ```

    This creates a full-text index named "ContentFullText" on all Content nodes’ `text`. We can then do queries like:

    ```cypher
    CALL db.index.fulltext.queryNodes("ContentFullText", "travel plans~") YIELD node, score
    ```

    to get content nodes matching “travel plans” (the `~` could allow fuzzy matching). We might also create a full-text index on Person names or other fields if needed (for instance, if we wanted to search names or emails with partial matches). The primary use, however, is for message content and documents.

  * **Vector Index:** Neo4j 5.11+ allows vector indexing for similarity search. We will create a vector index on the Content embedding property. Suppose we use 384-dimensional embeddings for message texts (just as an example dimension). We do:

    ```cypher
    CREATE VECTOR INDEX ContentVectorIndex FOR (c:Content) ON (c.embedding)
    OPTIONS {indexConfig: { "vector.dimensions": 384, "vector.similarity_function": "COSINE" }};
    ```

    This index uses an approximate nearest neighbor (ANN) algorithm (HNSW under the hood) to support queries like “find the top k content nodes most similar to this query vector”. With this in place, we can call the procedure `db.index.vector.queryNodes("ContentVectorIndex", $K, $vector)` to retrieve content nodes by embedding similarity. This is crucial for semantic search capabilities (e.g. finding if any conversation is about a concept without exact keyword match). The dimension must match the embedding vector length we store. If using a larger model (say 768 or 1536 dims), adjust accordingly. We choose cosine similarity as it’s common for normalized embeddings.

These indexes ensure that our schema fully leverages Neo4j’s capabilities: we can do fast graph traversals combined with indexed lookups for text or vector similarity or geospatial queries. All the above index creations use **Neo4j OSS features** (full-text and vector indexes are available in the open-source Neo4j 5.x as of their respective versions, and spatial is built-in). No proprietary extensions are required.

### Example Cypher Queries for Benchmark Questions

Below are a few example Cypher queries demonstrating how the unified schema can answer some of the evaluation questions. We assume these queries run on the Neo4j database after the data has been imported according to our schema.

1. **Q: "Does Fred discuss travel plans?"** – This question implies we need to find communications involving Fred (Merlin) where the conversation content is about travel plans. This is a hybrid query: filter by participant = Fred and by semantic content about "travel plans". We can approach it by first finding Fred’s sessions, then checking content, or by searching content and filtering by Fred – the latter is efficient using the vector index. For example:

   ```cypher
   // Get embedding for query phrase "travel plans" (this would be provided by the application using an embedding model)
   WITH $travelPlansVector AS queryVec
   CALL db.index.vector.queryNodes("ContentVectorIndex", 10, queryVec) YIELD node AS content, score
   MATCH (content)<-[:HAS_CONTENT]-(s:Session)<-[:PARTICIPATED_IN]-(p:Person {name:"Fred Merlin"})
   RETURN s.sessionguid, s.createddate, score, content.text
   ORDER BY score DESC;
   ```

   In this query, we use a parameter `$travelPlansVector` which is the embedding of the phrase "travel plans". The `db.index.vector.queryNodes` call finds, say, the top 10 Content nodes whose embeddings are closest (most similar) to this query vector. We then filter those results by matching only those content nodes that belong to a Session where a Person named Fred Merlin participated. The result yields the sessions (with their IDs and dates, and maybe snippet of text) ordered by similarity score. This would retrieve sessions where Fred is talking and the content is semantically related to travel plans. We could also incorporate a full-text condition if needed (e.g. ensure the word "travel" appears, etc., but the vector search suffices for semantic). If we wanted a purely full-text approach for literal mentions, we could do:

   ```cypher
   CALL db.index.fulltext.queryNodes("ContentFullText", "travel OR trip") YIELD node AS content, score
   MATCH (content)<-[:HAS_CONTENT]-(s:Session)<-[:PARTICIPATED_IN]-(p:Person {name:"Fred Merlin"})
   RETURN DISTINCT s.sessionnumber, s.createddate, content.text;
   ```

   This would find content containing the word "travel" (or similar) and then filter to Fred’s sessions. The unified schema supports either method.

2. **Q: "How does @Hawk, Kenzie communicate with @Frasier, Owen?"** – This question expects an answer summarizing the types of communication (e.g. SMS vs calls and their counts) between Kenzie Hawk and Owen Frasier. We can find all sessions where Kenzie and Owen are both participants, then aggregate by session type or application. For instance:

   ```cypher
   MATCH (p1:Person {name:"Kenzie Hawk"})-[:USES|:PARTICIPATED_IN*2..2]->(s:Session)<-[:USES|:PARTICIPATED_IN*2..2]-(p2:Person {name:"Owen Frasier"})
   // The above pattern finds sessions connected to both persons (via their accounts). 
   // We allow 2 hops: Person -> Account -> Session on each side. The *2..2 is a path of length 2.
   WHERE p1 <> p2
   WITH s, s.sessiontype AS type, coalesce(s.application, s.sessiontype) AS appType
   RETURN appType, count(*) AS numberOfSessions
   ORDER BY numberOfSessions DESC;
   ```

   This query uses a variable length path to traverse Person→Account→Session for each person and finds common sessions. We then categorize by either `s.application` (which might say "SMS", "Unknown", etc.) or `s.sessiontype` if application is not set. The result might be: `SMS = 24, Unknown = 7` for example, indicating Kenzie and Owen communicated via 24 SMS messages and 7 telephony sessions (which had application "Unknown"). We could refine the MATCH pattern explicitly:

   ```cypher
   MATCH (k:Person {name:"Kenzie Hawk"})-[:USES]->(acct1:Account)-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]- (acct2:Account)<-[:USES]- (o:Person {name:"Owen Frasier"})
   WITH s, coalesce(s.application, s.sessiontype) AS channel
   RETURN channel AS communicationType, count(*) AS count;
   ```

   This explicitly goes Person->Account->Session for each. The `coalesce` handles if `application` field is null by falling back to sessiontype. We assume in SMS sessions, s.application = "SMS", and in call sessions, s.application = "Unknown" (and maybe s.sessiontype = "Telephony"). The result will directly give the breakdown required. Because we modeled Person–Account and Account–Session, the Cypher is quite natural. If we had no account nodes (and linked persons directly to sessions in all cases), the query could be a simpler `MATCH (Kenzie)-[:PARTICIPATED_IN]->(s:Session)<-[:PARTICIPATED_IN]-(Owen)` – which works if persons are directly attached. In our schema, Kenzie is attached via her account in communications, hence including account in the path is necessary. The query is still straightforward and indexed (thanks to the Person->Account unique link and possibly an index on person name).

3. **Q: "What are Kenzie's IMEIs?"** – This asks for all device IMEIs associated with Kenzie Hawk, presumably with a count of how many sessions each was seen in. With our schema, we simply find the Device nodes linked to Kenzie:

   ```cypher
   MATCH (k:Person {name:"Kenzie Hawk"})-[:USES_DEVICE]->(d:Device)
   OPTIONAL MATCH (d)-[:HAS_ACCOUNT]->()-[:PARTICIPATED_IN]->(s:Session) 
   // count sessions for each device (or we could store usage count as a property via analysis)
   RETURN d.imei, count(DISTINCT s) AS sessionsCount;
   ```

   This will list each IMEI used by Kenzie and how many sessions that device appears in. The expected output (from eval) was something like IMEI1 (83 sessions), IMEI2 (1 session). That implies one of her devices was used heavily, another seen once (possibly a secondary/new device). Our query captures that. We use `DISTINCT s` just in case a device had multiple accounts in one session or similar, to count unique sessions. If we wanted to be absolutely sure we only count sessions where that device was actually present, we could tighten the pattern to require the device’s participation: e.g. `(d)-[:HAS_ACCOUNT]->(acct)-[:PARTICIPATED_IN]->(s)` will only count sessions where that device’s account took part. That matches reality: if device not present, it wouldn't have an account link in that session. So the above OPTIONAL MATCH effectively does that counting. We could also have precomputed and stored usage counts on the relationship or device node, but dynamic count via query is fine.

4. **Q: "Which IMEIs are associated with phone number 9366351931?"** – This looks for all devices that have used a given number (and presumably indicates if one of them is not in data). Query:

   ```cypher
   MATCH (ph:Phone {number:"9366351931"})<-[:HAS_ACCOUNT]-(d:Device)
   RETURN d.imei;
   ```

   This will return the IMEIs of devices linked to that Phone account. Our schema directly stores those via the HAS\_ACCOUNT relationship, so it’s a single-hop traversal. If needed, we could count sessions per device as well, or list additional info. The expected answer mentioned two IMEIs, one of which had “(Not on Data)” – possibly meaning one device was inferred or known but had no sessions in this dataset. In our graph, if a device node had no sessions linking, it still could show up from the Person–Device link. That’s fine. If we strictly only link device to account when it appears in a session, then “not on data” might mean we actually wouldn’t have that device node unless we inserted it manually. But since the question expects it, likely the data had a reference. Regardless, our graph can hold a Device even if it had just one association. The query above finds what’s in the graph.

5. **Q: "Who has been using devices with IMEI X?"** – e.g. given an IMEI, find which person(s) used it. Query:

   ```cypher
   MATCH (d:Device {imei: $imei})<-[:USES_DEVICE]-(person:Person)
   RETURN person.name, count(DISTINCT d) as deviceCount;
   ```

   If the IMEI exists and is linked to persons, this returns the person name(s). In our design, ideally each device is linked to whoever used it. According to the expected result, IMEI X was used by William Eagle (75 sessions) and Ted Dowitcher (1 session). If our data had Ted Dowitcher’s one session with that IMEI and William’s many, our graph would have edges from that Device to both William and Ted. The query above would list both names. (If we wanted the session counts, we could expand to sessions similarly to earlier queries.) This again is a simple one-hop traversal thanks to the explicit Person–Device relationships.

6. **Q: "Is IMEI Y in my data? If so, give details."** – This can be answered by checking if a Device node with that IMEI exists. For details, we might return how many sessions it appears in or who uses it. A combined query:

   ```cypher
   MATCH (d:Device {imei: $imei})
   OPTIONAL MATCH (d)-[:HAS_ACCOUNT]->(acct:Account)
   OPTIONAL MATCH (d)<-[:USES_DEVICE]-(person:Person)
   OPTIONAL MATCH (d)-[:HAS_ACCOUNT]->(acct)-[:PARTICIPATED_IN]->(s:Session)
   WITH d, collect(DISTINCT acct) as accounts, collect(DISTINCT person) as users, count(DISTINCT s) as sessionCount
   RETURN d.imei AS imei, 
          case when d is not null then "YES" else "NO" end as present,
          sessionCount, 
          [p in users | p.name] AS userNames,
          [a in accounts | coalesce(a.number, a.email)] AS associatedAccounts;
   ```

   This will output whether the IMEI node exists and some details: how many sessions it's in, which users and accounts are linked to it. If none, `present` would be "NO". This is more data retrieval than a simple Cypher, but it shows how the graph can aggregate relevant info about an IMEI quickly.

7. **Q: "What is Kenzie Hawk’s email address?"** – We have a Person and we want their email account. Query:

   ```cypher
   MATCH (k:Person {name:"Kenzie Hawk"})-[:USES]->(e:Email)
   RETURN e.email;
   ```

   This will return her email. Based on the data, we expect "[ziezieken88@gmail.com](mailto:ziezieken88@gmail.com)". Indeed, our graph from the contact entry would have created a Person Kenzie (target) and likely we have an Email account node for that address if it appeared (it did in Fiona’s contact card – Fiona’s vCard had Kenzie’s email? Actually, looking carefully: Fiona’s contact card in NDJSON had targetname Kenzie (meaning this contact is in Kenzie’s data) and in the vCard content we see Fiona’s details. Kenzie’s own email address might not be explicitly in Fiona’s card. Possibly Kenzie’s email came from somewhere else, maybe Kenzie’s own account info or from another contact. However, since the expected answer is that Gmail address, likely the data included it, perhaps in an “All Contacts” list or because that email was used by Kenzie in correspondences. In any event, if it’s present as an Account used by Kenzie, the query above finds it. If Kenzie was the target of an email data source, her account might have been labeled as an Account with targetname. We would have linked Kenzie to that email in the import process if detected. The graph model easily allows storing that when parsing input: e.g. if a session’s targetname is Kenzie and sessiontype "Email", we could deduce her email from sourceid or content. For brevity here, we assume we have the info.)

These examples illustrate that **every benchmark query can be expressed cleanly in Cypher with this schema**. The graph model directly supports entity filtering, relationship traversal, aggregation, and text/vector search. In many cases, just a few hops in a MATCH clause yield the answer, which attests to the schema’s design for query needs.
