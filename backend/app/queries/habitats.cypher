// Queries for Habitat exploration and filtering

// Get animals by habitat name
MATCH (a:Animal)-[:LIVES_IN]->(h:Habitat)
WHERE toLower(h.name) = toLower($habitat_name)
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
RETURN a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       c.name AS className,
       cs.name AS conservationStatus,
       d.name AS diet,
       h.name AS habitat
ORDER BY a.name;

// Get animals by conservation status
MATCH (a:Animal)-[:HAS_STATUS]->(cs:ConservationStatus)
WHERE toLower(cs.name) = toLower($status_name)
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
RETURN a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       c.name AS className,
       cs.name AS conservationStatus,
       d.name AS diet,
       collect(DISTINCT h.name) AS habitats
ORDER BY a.name;

// Get animals by diet category
MATCH (a:Animal)-[:HAS_DIET]->(d:Diet)
WHERE toLower(d.name) = toLower($diet_name)
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
RETURN a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       c.name AS className,
       cs.name AS conservationStatus,
       d.name AS diet,
       collect(DISTINCT h.name) AS habitats
ORDER BY a.name;

// Get animals by continent
MATCH (a:Animal)-[:FOUND_IN]->(ct:Continent)
WHERE toLower(ct.name) = toLower($continent_name)
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
RETURN a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       c.name AS className,
       cs.name AS conservationStatus,
       d.name AS diet,
       collect(DISTINCT h.name) AS habitats
ORDER BY a.name;
