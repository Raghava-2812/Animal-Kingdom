// Queries for Animal search, details, and filtering

// Search animals by name or scientific name
MATCH (a:Animal)
WHERE toLower(a.name) CONTAINS toLower($query) 
   OR toLower(a.scientificName) CONTAINS toLower($query)
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

// Get detailed animal information by ID
MATCH (a:Animal {id: $animal_id})
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)
OPTIONAL MATCH (s)-[:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[:EATS]->(f:Food)
OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
RETURN a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       s.name AS species,
       s.scientificName AS speciesScientificName,
       c.name AS className,
       d.name AS diet,
       cs.name AS conservationStatus,
       collect(DISTINCT h.name) AS habitats,
       collect(DISTINCT f.name) AS foodSources,
       collect(DISTINCT ct.name) AS continents;

// Get all animals with primary metadata
MATCH (a:Animal)
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
RETURN a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       c.name AS className,
       cs.name AS conservationStatus,
       d.name AS diet,
       collect(DISTINCT h.name) AS habitats,
       collect(DISTINCT ct.name) AS continents
ORDER BY a.name;
