# 🐾 Animal Kingdom Knowledge Graph

> **"Explore the relationships between animals, habitats, diets and conservation status."**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Neo4j](https://img.shields.io/badge/Graph_Database-Neo4j_5-008CC1.svg?style=flat&logo=neo4j)](https://neo4j.com)
[![Cypher](https://img.shields.io/badge/Query_Language-Cypher-4584b6.svg?style=flat)](https://neo4j.com/developer/cypher/)
[![React](https://img.shields.io/badge/Frontend-React_19-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS_v4-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)

---

## 1. Project Statement & Academic Purpose

> **Academic Statement:**
> *"Animal Kingdom Knowledge Graph is a graph-based information system that models animals and their relationships with species, taxonomy, habitats, diets, food sources, geographical regions and conservation status. Neo4j stores this interconnected information, while Python FastAPI processes user requests and executes Cypher queries. The React interface allows users to search animals, ask knowledge-based questions and visually explore relationships."*

### Core Design Principle: Entity → Relationship → Entity
Traditional relational applications decompose domain models into isolated tables joined by foreign keys. In contrast, this project represents wildlife ecology as an interconnected property graph:

$$\text{Tiger} \xrightarrow{\text{BELONGS\_TO\_SPECIES}} \text{Panthera tigris} \xrightarrow{\text{BELONGS\_TO\_CLASS}} \text{Mammal}$$
$$\text{Tiger} \xrightarrow{\text{LIVES\_IN}} \text{Forest} \quad \bullet \quad \text{Tiger} \xrightarrow{\text{EATS}} \text{Deer} \quad \bullet \quad \text{Tiger} \xrightarrow{\text{HAS\_STATUS}} \text{Endangered}$$

---

## 2. System Architecture

```
User
  ↓
React 19 Frontend (Tailwind CSS, Vite, SVG Graph Engine)
  ↓ [REST APIs / JSON]
Python FastAPI Backend
  ↓ [Official Neo4j Driver]
Neo4j Graph Database (Bolt Protocol)
  ↓ [Cypher Query Engine]
Graph Traversal & Subgraph Extraction
  ↓
FastAPI Services
  ↓
React Knowledge Graph Visualization & Cypher Inspector
```

---

## 3. Technology Stack

* **Frontend:** React 19, React Router v7, Tailwind CSS v4, Lucide React, Vite.
* **Backend:** Python 3.10+, FastAPI, Pydantic v2, Uvicorn, Python-dotenv.
* **Database & Driver:** Neo4j Community Edition 5.x, Official Neo4j Python Driver (`neo4j>=5.18.0`).
* **Query Language:** Cypher.
* **Testing:** Pytest, HTTPX TestClient.

---

## 4. Knowledge Graph Schema

### Node Labels
* **`Animal`**: `id`, `name`, `scientificName`, `description`, `averageLifespan`, `imageUrl`
* **`Species`**: `id`, `name`, `scientificName`
* **`Class`**: `id`, `name` (e.g. *Mammal, Bird, Reptile, Amphibian, Fish, Insect*)
* **`Habitat`**: `id`, `name`, `description` (e.g. *Forest, Grassland, Ocean, River, Wetland, Savanna, Polar Tundra*)
* **`Diet`**: `id`, `name` (e.g. *Carnivore, Herbivore, Omnivore, Insectivore*)
* **`Food`**: `id`, `name` (e.g. *Deer, Grass, Fish, Insects, Bamboo, Krill*)
* **`ConservationStatus`**: `id`, `name` (e.g. *Least Concern, Vulnerable, Endangered, Critically Endangered*)
* **`Continent`**: `id`, `name` (e.g. *Asia, Africa, Europe, North America, South America, Australia, Antarctica*)

### Relationships
* `(:Animal)-[:BELONGS_TO_SPECIES]->(:Species)`
* `(:Species)-[:BELONGS_TO_CLASS]->(:Class)`
* `(:Animal)-[:LIVES_IN]->(:Habitat)`
* `(:Animal)-[:HAS_DIET]->(:Diet)`
* `(:Animal)-[:EATS]->(:Food)`
* `(:Animal)-[:HAS_STATUS]->(:ConservationStatus)`
* `(:Animal)-[:FOUND_IN]->(:Continent)`
* `(:Habitat)-[:LOCATED_IN]->(:Continent)`

---

## 5. Prerequisites & Environment Setup

### 5.1. Clone / Workspace
Navigate into the repository directory:
```bash
cd "d:\KG_Projects\Animal Kingdom"
```

### 5.2. Neo4j Setup
You can run Neo4j using Docker (included `docker-compose.yml`) or via Neo4j Desktop / AuraDB:

**Using Docker:**
```bash
docker compose up -d
```
Neo4j Browser will be accessible at: `http://localhost:7474`
* Username: `neo4j`
* Password: `password123`

---

## 6. Backend Setup & Seeding

### 6.1. Environment Configuration
Create or inspect `backend/.env`:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123
NEO4J_DATABASE=neo4j
APP_HOST=0.0.0.0
APP_PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 6.2. Install Python Dependencies
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1    # On Windows
# source venv/bin/activate     # On Linux / macOS

pip install -r backend/requirements.txt
```

### 6.3. Seed the Knowledge Graph
Populate Neo4j with 38 diverse animals, taxonomies, habitats, and relationships:
```bash
python -m backend.seed.seed_data
```

### 6.4. Run Backend Server
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation will be available at: `http://localhost:8000/docs`.

### 6.5. Run Backend Tests
```bash
python -m pytest backend/tests
```

---

## 7. Frontend Setup

### 7.1. Install Frontend Dependencies
```bash
cd frontend
npm.cmd install
```

### 7.2. Start Vite Development Server
```bash
npm.cmd run dev
```
Open your browser at: `http://localhost:5173`

---

## 8. Interactive Features & Demonstration Workflow

### Step 1: Open the Application
Launch the home page to view dynamic Neo4j statistics (38 Animals, 38 Species, 9 Habitats, 28 Food sources, 9 Endangered species).

### Step 2: Search for an Animal
Navigate to **Explore Animals** and search for `Tiger`.

### Step 3: View Animal Details
Click **View Details** to inspect Tiger's taxonomy, diet, habitats, and IUCN classification.

### Step 4: Explore Relationships Graph
Click **Explore Relationships Graph** to inspect the interactive SVG neighborhood:
$$\text{Tiger} \longrightarrow \text{Panthera tigris, Mammal, Forest, Carnivore, Deer, Endangered, Asia}$$
* Pan, zoom, and click nodes to view properties.

### Step 5: Graph Traversal Discovery
Click the **Forest** node in the graph viewer and click **Explore all animals in Forest** to discover other forest-dwelling animals (Elephant, Panda, Gorilla, Leopard).

### Step 6: Ask the Knowledge Graph
Open **Ask Knowledge Graph**:
1. Click the chip: *"Show endangered animals that live in forests"*.
2. Click **Ask Graph**.
3. View the extracted constraints: `status = 'Endangered'`, `habitat = 'Forest'`.
4. Inspect the generated Cypher query in the code box.
5. Review the result cards retrieved from the graph.

---

## 9. API Overview

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Health status & Neo4j connectivity |
| `/api/dashboard/stats` | GET | Aggregated graph counts |
| `/api/animals` | GET | Multi-facet animal search and filtering |
| `/api/animals/{id}` | GET | Detailed entity information & taxonomy |
| `/api/animals/{id}/graph` | GET | Subgraph nodes and relationships for visualization |
| `/api/search?q={query}` | GET | Common & scientific name text search |
| `/api/habitats/{name}/animals` | GET | Animals living in specified habitat |
| `/api/conservation/{status}/animals` | GET | Animals with specified IUCN threat level |
| `/api/diets/{name}/animals` | GET | Animals categorized by diet |
| `/api/continents/{name}/animals` | GET | Animals distributed in continent |
| `/api/queries/examples` | GET | Predefined academic questions |
| `/api/queries/ask` | POST | Translates question to Cypher and executes |

---

## 10. Sample Cypher Queries

### Endangered Forest Animals
```cypher
MATCH (a:Animal)-[:LIVES_IN]->(h:Habitat),
      (a)-[:HAS_STATUS]->(s:ConservationStatus)
WHERE h.name = "Forest" AND s.name = "Endangered"
RETURN a.name;
```

### Carnivorous Mammals
```cypher
MATCH (a:Animal)-[:HAS_DIET]->(d:Diet),
      (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
WHERE d.name = "Carnivore" AND c.name = "Mammal"
RETURN a.name;
```

### Animals that Eat Fish
```cypher
MATCH (a:Animal)-[:EATS]->(f:Food)
WHERE f.name = "Fish"
RETURN a.name;
```

---

## 11. Project Directory Structure

```
Animal Kingdom/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application setup & CORS
│   │   ├── config.py                   # Pydantic configuration & dotenv
│   │   ├── database/
│   │   │   ├── neo4j.py                # Official Neo4j Python driver manager
│   │   │   └── schema.py               # Constraints and indexes
│   │   ├── models/
│   │   │   ├── animal.py               # DTO schemas for animals & stats
│   │   │   ├── query.py                # Natural language query schemas
│   │   │   └── graph.py                # Graph visualization schemas
│   │   ├── routes/
│   │   │   ├── animals.py              # Animal listing & details endpoints
│   │   │   ├── dashboard.py            # Graph stats endpoint
│   │   │   ├── search.py               # Text search endpoint
│   │   │   ├── habitats.py             # Categorical exploration endpoints
│   │   │   ├── queries.py              # Natural language query endpoint
│   │   │   └── graph.py                # Subgraph visualization endpoints
│   │   ├── services/
│   │   │   ├── animal_service.py       # Entity & aggregation queries
│   │   │   ├── search_service.py       # Facet queries
│   │   │   ├── query_service.py        # Question-to-Cypher mapping engine
│   │   │   └── graph_service.py        # Subgraph builders
│   │   └── queries/
│   │       ├── animals.cypher          # Raw Cypher templates
│   │       ├── dashboard.cypher
│   │       ├── habitats.cypher
│   │       └── graph.cypher
│   ├── seed/
│   │   ├── animals_data.py             # Curated dataset of 38 animals
│   │   └── seed_data.py                # Database population script
│   ├── tests/
│   │   └── test_api.py                 # Pytest test suite (14 test cases)
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx              # Navigation & connection pulse
│   │   │   ├── SearchBar.jsx           # Live search input
│   │   │   ├── StatCard.jsx            # Metric cards
│   │   │   ├── AnimalCard.jsx          # Animal card with badges
│   │   │   ├── FilterPanel.jsx         # Multi-facet filter controls
│   │   │   ├── QueryBox.jsx            # NL query input & example chips
│   │   │   ├── QueryResult.jsx         # Cypher inspector & results grid
│   │   │   └── GraphViewer.jsx         # Interactive SVG graph visualizer
│   │   ├── pages/
│   │   │   ├── Home.jsx                # Academic dashboard & stats
│   │   │   ├── Explore.jsx             # Animal search & catalog
│   │   │   ├── AnimalDetails.jsx       # Taxonomy & relationship viewer
│   │   │   └── AskKnowledgeGraph.jsx   # Natural language Cypher interface
│   │   ├── services/
│   │   │   └── api.js                  # Frontend API client
│   │   ├── App.jsx                     # Route definitions
│   │   ├── index.css                   # Tailwind styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── HLD.md                          # High-level architecture & Mermaid diagrams
│   ├── KNOWLEDGE_GRAPH_MODEL.md        # Graph ontology & constraints
│   ├── API_DOCUMENTATION.md            # REST API specifications
│   └── CYPHER_QUERIES.md               # Cypher reference catalog
├── docker-compose.yml                  # Neo4j community container definition
├── .gitignore
└── README.md
```

---

## 12. Future Enhancements

1. **Biodiversity API Ingestion**: Integrate GBIF (Global Biodiversity Information Facility) live data feeds.
2. **Ontology Reasoning**: Implement OWL/RDFS reasoning rules over taxonomic hierarchies.
3. **Multilingual Query Support**: Expand natural language entity extraction to Spanish, French, and Hindi.
4. **LLM-assisted Cypher Generation with Guardrails**: Add LLM-based translation validated against graph schema and read-only query safety rules.
5. **Geospatial Map Integration**: Plot habitat coordinates on interactive Leaflet/Mapbox maps.
6. **Graph Algorithms**: Run Neo4j GDS (Graph Data Science) PageRank and Louvain community detection to detect keystone species in ecosystems.
