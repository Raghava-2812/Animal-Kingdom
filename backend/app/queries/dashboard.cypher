// Dashboard statistics queries

// 1. Total count of Animal nodes
MATCH (a:Animal)
RETURN count(a) AS totalAnimals;

// 2. Total count of Species nodes
MATCH (s:Species)
RETURN count(s) AS totalSpecies;

// 3. Total count of Habitat nodes
MATCH (h:Habitat)
RETURN count(h) AS totalHabitats;

// 4. Total count of Food items
MATCH (f:Food)
RETURN count(f) AS totalFoods;

// 5. Total count of Endangered / Critically Endangered animals
MATCH (a:Animal)-[:HAS_STATUS]->(s:ConservationStatus)
WHERE s.name IN ["Endangered", "Critically Endangered"]
RETURN count(DISTINCT a) AS totalEndangeredAnimals;

// 6. Total count of Continents
MATCH (c:Continent)
RETURN count(c) AS totalContinents;

// Combined Dashboard Aggregation
MATCH (a:Animal)
WITH count(a) AS totalAnimals
MATCH (s:Species)
WITH totalAnimals, count(s) AS totalSpecies
MATCH (h:Habitat)
WITH totalAnimals, totalSpecies, count(h) AS totalHabitats
MATCH (f:Food)
WITH totalAnimals, totalSpecies, totalHabitats, count(f) AS totalFoods
MATCH (c:Continent)
WITH totalAnimals, totalSpecies, totalHabitats, totalFoods, count(c) AS totalContinents
OPTIONAL MATCH (ea:Animal)-[:HAS_STATUS]->(st:ConservationStatus)
WHERE st.name IN ["Endangered", "Critically Endangered"]
RETURN totalAnimals, totalSpecies, totalHabitats, totalFoods, totalContinents, count(DISTINCT ea) AS totalEndangeredAnimals;
