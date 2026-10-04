// Graph visualization extraction queries

// Subgraph for a specific animal (node and 1-hop relationships)
MATCH (a:Animal {id: $animal_id})
OPTIONAL MATCH (a)-[r1:BELONGS_TO_SPECIES]->(s:Species)
OPTIONAL MATCH (s)-[r2:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[r3:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[r4:HAS_DIET]->(d:Diet)
OPTIONAL MATCH (a)-[r5:EATS]->(f:Food)
OPTIONAL MATCH (a)-[r6:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[r7:FOUND_IN]->(ct:Continent)
RETURN a, r1, s, r2, c, r3, h, r4, d, r5, f, r6, cs, r7, ct;

// Subgraph for global Knowledge Graph sample
MATCH (a:Animal)
WITH a LIMIT 12
OPTIONAL MATCH (a)-[r1:BELONGS_TO_SPECIES]->(s:Species)-[r2:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[r3:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[r4:HAS_DIET]->(d:Diet)
OPTIONAL MATCH (a)-[r5:EATS]->(f:Food)
OPTIONAL MATCH (a)-[r6:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[r7:FOUND_IN]->(ct:Continent)
RETURN a, r1, s, r2, c, r3, h, r4, d, r5, f, r6, cs, r7, ct;
