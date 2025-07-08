# Ultra Simple Topic Naming Guide for Analysts

**Problem**: Query returns raw conversation clusters - how do analysts name topics?

## Solution 1: Manual Review (Current Approach)

Looking at your actual data, analysts can quickly identify patterns:

| Cluster Sample | Size | Pattern Recognition | Suggested Topic Name |
|----------------|------|-------------------|-------------------|
| "Hey, Freddy. You still good to me tonight?" | 99 | Freddy, Benny, meetings | **Freddy Network Meetings** |
| "Benny and I...meet with Freddy...that shipment" | 98 | shipment, business | **Shipment Coordination** |
| "trip...March 16 to 30...flights from kayak" | 76 | travel dates, Bangkok | **Bangkok Trip Planning** |
| "My mom's really sick...take her to clinic" | 50 | family, health | **Family Health Issues** |
| "Getting coffee...part for the truck" | 38 | daily activities | **Daily Operations** |
| "Supplier problem...Eagles Maintenance" | 25 | business name | **Eagles Landscaping Business** |

## Solution 2: Add Word Frequency (Recommended)

Modify your query to show most frequent words per cluster:

```cypher
// After collecting cluster_items, add:
WITH seed, cluster_items,
     // Get all text from cluster
     reduce(text = '', item IN cluster_items | text + ' ' + item.text) AS cluster_text

// Count word frequencies
UNWIND split(toLower(cluster_text), ' ') AS word
WITH seed, cluster_items, word
WHERE size(word) > 4 
  AND NOT word IN ['about', 'there', 'would', 'could', 'should', 'hello']
WITH seed, cluster_items, word, count(*) AS freq
ORDER BY freq DESC

// Return top 5 words per cluster
WITH seed, cluster_items, collect(word)[0..5] AS top_words

RETURN size(cluster_items) AS size,
       top_words AS frequent_words,  // e.g., ['freddy', 'meeting', 'tonight', 'benny', 'shipment']
       substring(seed.text, 0, 100) AS example
```

## Solution 3: Pattern-Based Naming (Simplest)

Since you're analyzing surveillance data, use this decision tree:

1. **Contains person names** (Freddy, Benny, etc.) → "[Name] Network"
2. **Contains locations** (Bangkok, Columbia) → "[Location] Operations"  
3. **Contains business names** (Eagles) → "[Business] Activities"
4. **Contains activities** (meeting, shipment, betting) → "[Activity] Coordination"
5. **Contains dates/times** → "Scheduled Events"
6. **Everything else** → "General Communications"

## For Your Specific Results

Based on your JSON data, here's how analysts would name topics:

```
Cluster 1 (99 convos): "Freddy" appears → "Freddy Network Operations"
Cluster 2 (98 convos): "shipment" + "Benny" → "Shipment Coordination" 
Cluster 3 (76 convos): "trip" + dates → "Travel Planning"
Cluster 4 (50 convos): "mom's sick" → "Family/Health Matters"
Cluster 5 (38 convos): "coffee" + "truck" → "Daily Activities"
Cluster 6 (25 convos): "Eagles Maintenance" → "Landscaping Business"
```

## Implementation Choice

**For immediate use**: Train analysts to use the pattern-based naming (Solution 3)

**For automation**: Add word frequency counting to your query (Solution 2)

**Key insight**: You don't need AI to name topics - frequent words and simple patterns are enough!