# Cypher Queries Reference — Animal Kingdom Knowledge Graph

This document details the Cypher queries used by the Python backend when querying the **Neo4j Knowledge Graph**.

---

## 1. Core Graph Queries

### 1.1. Retrieve All Animals
```cypher
MATCH (a:Animal)
RETURN a.id AS id, a.name AS name, a.scientificName AS scientificName;
```

### 1.2. Retrieve Endangered Animals
```cypher
MATCH (a:Animal)-[:HAS_STATUS]->(s:ConservationStatus)
WHERE s.name = "Endangered"
RETURN a.name AS animal, s.name AS status;
```

### 1.3. Animals Living in Forests
```cypher
MATCH (a:Animal)-[:LIVES_IN]->(h:Habitat)
WHERE h.name = "Forest"
RETURN a.name AS animal, h.name AS habitat;
```

### 1.4. Carnivorous Mammals
```cypher
MATCH (a:Animal)-[:HAS_DIET]->(d:Diet),
      (a)-[:BELONGS_TO_SPECIES]->(s:Species),
      (s)-[:BELONGS_TO_CLASS]->(c:Class)
WHERE d.name = "Carnivore"
  AND c.name = "Mammal"
RETURN a.name AS animal, d.name AS diet, c.name AS class;
```

### 1.5. Endangered Forest Animals
```cypher
MATCH (a:Animal)-[:LIVES_IN]->(h:Habitat),
      (a)-[:HAS_STATUS]->(s:ConservationStatus)
WHERE h.name = "Forest"
  AND s.name = "Endangered"
RETURN a.name AS animal, h.name AS habitat, s.name AS status;
```

### 1.6. Animals that Eat Fish
```cypher
MATCH (a:Animal)-[:EATS]->(f:Food)
WHERE f.name = "Fish"
RETURN a.name AS animal, f.name AS foodSource;
```

### 1.7. Animals Found in Asia
```cypher
MATCH (a:Animal)-[:FOUND_IN]->(c:Continent)
WHERE c.name = "Asia"
RETURN a.name AS animal, c.name AS continent;
```

### 1.8. Animals that Live in both Forests and Grasslands
```cypher
MATCH (a:Animal)-[:LIVES_IN]->(h1:Habitat),
      (a)-[:LIVES_IN]->(h2:Habitat)
WHERE h1.name = "Forest"
  AND h2.name = "Grassland"
RETURN a.name AS animal;
```

---

## 2. Dashboard Aggregations

```cypher
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
RETURN totalAnimals,
       totalSpecies,
       totalHabitats,
       totalFoods,
       totalContinents,
       count(DISTINCT ea) AS totalEndangeredAnimals;
```

---

## 3. Subgraph Extraction for Graph Visualization

```cypher
MATCH (a:Animal {id: $animal_id})
OPTIONAL MATCH (a)-[r1:BELONGS_TO_SPECIES]->(s:Species)
OPTIONAL MATCH (s)-[r2:BELONGS_TO_CLASS]->(c:Class)
OPTIONAL MATCH (a)-[r3:LIVES_IN]->(h:Habitat)
OPTIONAL MATCH (a)-[r4:HAS_DIET]->(d:Diet)
OPTIONAL MATCH (a)-[r5:EATS]->(f:Food)
OPTIONAL MATCH (a)-[r6:HAS_STATUS]->(cs:ConservationStatus)
OPTIONAL MATCH (a)-[r7:FOUND_IN]->(ct:Continent)
RETURN a, r1, s, r2, c, r3, h, r4, d, r5, f, r6, cs, r7, ct;
```
