# REST API Documentation — Animal Kingdom Knowledge Graph

Base URL: `http://localhost:8000`

---

## 1. System Health

### `GET /api/health`
Checks backend responsiveness and Neo4j connection status.

**Response (200 OK):**
```json
{
  "status": "online",
  "neo4jConnected": true,
  "databaseUri": "bolt://localhost:7687",
  "environment": "development"
}
```

---

## 2. Dashboard

### `GET /api/dashboard/stats`
Aggregates live counts across graph node categories directly from Neo4j.

**Response (200 OK):**
```json
{
  "totalAnimals": 38,
  "totalSpecies": 38,
  "totalHabitats": 9,
  "totalFoods": 28,
  "totalEndangeredAnimals": 9,
  "totalContinents": 7,
  "neo4jConnected": true
}
```

---

## 3. Animal Exploration & Details

### `GET /api/animals`
List animals with optional multi-facet filtering.

**Query Parameters:**
* `class` *(optional)*: e.g. `Mammal`, `Bird`, `Reptile`
* `habitat` *(optional)*: e.g. `Forest`, `Ocean`
* `diet` *(optional)*: e.g. `Carnivore`, `Herbivore`
* `status` *(optional)*: e.g. `Endangered`, `Vulnerable`
* `continent` *(optional)*: e.g. `Asia`, `Africa`

**Response (200 OK):**
```json
[
  {
    "id": "animal_tiger",
    "name": "Tiger",
    "scientificName": "Panthera tigris",
    "description": "The largest living cat species...",
    "averageLifespan": 15,
    "imageUrl": "https://images.unsplash.com/...",
    "className": "Mammal",
    "conservationStatus": "Endangered",
    "diet": "Carnivore",
    "habitats": ["Forest", "Wetland"],
    "continents": ["Asia"]
  }
]
```

---

### `GET /api/animals/{animal_id}`
Returns complete entity information and connected graph properties for an animal.

**Path Parameters:**
* `animal_id`: e.g. `animal_tiger`

**Response (200 OK):**
```json
{
  "id": "animal_tiger",
  "name": "Tiger",
  "scientificName": "Panthera tigris",
  "description": "The largest living cat species...",
  "averageLifespan": 15,
  "imageUrl": "https://images.unsplash.com/...",
  "species": "Bengal / Siberian Tiger",
  "speciesScientificName": "Panthera tigris",
  "className": "Mammal",
  "diet": "Carnivore",
  "conservationStatus": "Endangered",
  "habitats": ["Forest", "Wetland"],
  "foodSources": ["Deer", "Wild Boar"],
  "continents": ["Asia"]
}
```

---

### `GET /api/animals/{animal_id}/graph`
Extracts subgraph nodes and labeled relationships formatted for graph visualization.

**Response (200 OK):**
```json
{
  "nodes": [
    {
      "id": "animal_tiger",
      "label": "Tiger",
      "type": "Animal",
      "properties": { "scientificName": "Panthera tigris", "lifespan": 15 }
    },
    {
      "id": "species_panthera_tigris",
      "label": "Bengal / Siberian Tiger",
      "type": "Species",
      "properties": {}
    },
    {
      "id": "habitat_forest",
      "label": "Forest",
      "type": "Habitat",
      "properties": {}
    }
  ],
  "relationships": [
    {
      "id": "rel_animal_tiger_species",
      "source": "animal_tiger",
      "target": "species_panthera_tigris",
      "type": "BELONGS_TO_SPECIES",
      "properties": {}
    },
    {
      "id": "rel_animal_tiger_habitat_forest",
      "source": "animal_tiger",
      "target": "habitat_forest",
      "type": "LIVES_IN",
      "properties": {}
    }
  ]
}
```

---

## 4. Search & Categorical Exploration

### `GET /api/search?q={query}`
Searches animals matching common name or binomial scientific name.

### `GET /api/habitats/{habitat_name}/animals`
Returns animals living in `{habitat_name}` (e.g. `Forest`, `Ocean`).

### `GET /api/conservation/{status}/animals`
Returns animals with IUCN status `{status}` (e.g. `Endangered`, `Vulnerable`).

### `GET /api/diets/{diet_name}/animals`
Returns animals having dietary strategy `{diet_name}` (e.g. `Carnivore`).

### `GET /api/continents/{continent_name}/animals`
Returns animals found in continent `{continent_name}` (e.g. `Asia`, `Africa`).

---

## 5. Ask Knowledge Graph (Cypher Engine)

### `GET /api/queries/examples`
Returns list of predefined natural language questions.

### `POST /api/queries/ask`
Maps natural language question to graph entities, generates Cypher, executes against Neo4j, and returns results.

**Request Body:**
```json
{
  "question": "Show endangered animals that live in forests"
}
```

**Response (200 OK):**
```json
{
  "question": "Show endangered animals that live in forests",
  "detectedFilters": {
    "status": "Endangered",
    "habitat": "Forest"
  },
  "cypherQuery": "MATCH (a:Animal),\n     (a)-[:HAS_STATUS]->(cs:ConservationStatus),\n     (a)-[:LIVES_IN]->(h:Habitat)\nWHERE cs.name = $status_name AND h.name = $habitat_name\n...",
  "results": [
    {
      "id": "animal_tiger",
      "name": "Tiger",
      "className": "Mammal",
      "conservationStatus": "Endangered",
      "diet": "Carnivore",
      "habitats": ["Forest", "Wetland"],
      "continents": ["Asia"]
    }
  ],
  "resultCount": 1,
  "explanation": "Identified graph constraints: status = 'Endangered', habitat = 'Forest'. Found 1 matching animal entities."
}
```
