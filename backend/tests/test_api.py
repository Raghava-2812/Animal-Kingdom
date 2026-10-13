"""
Integration and Unit Tests for Animal Kingdom Knowledge Graph API.

Tests API route behaviors using FastAPI's TestClient:
- System health status and Neo4j connectivity flag.
- Aggregate metrics on the dashboard statistics endpoint.
- Multi-faceted query filtering and full-text substring search.
- Deep entity retrieval and 404 error handling.
- Category endpoints (habitats, IUCN conservation statuses, diets, continents).
- Natural language to Cypher translation engine with entity verification.
- Graph visualization ego-network payloads.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.query_service import QueryService

client = TestClient(app)


# ---------------------------------------------------------------------------
# 1. Health and Dashboard Tests
# ---------------------------------------------------------------------------

def test_health_check():
    """Verify that the health check endpoint returns status 200 and operational details."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "neo4jConnected" in data


def test_dashboard_stats():
    """Verify that dashboard stats return accurate counts matching the graph model."""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["totalAnimals"] >= 30
    assert data["totalSpecies"] >= 30
    assert data["totalHabitats"] >= 5
    assert data["totalEndangeredAnimals"] >= 1


# ---------------------------------------------------------------------------
# 2. Animal Listing & Filtering Tests
# ---------------------------------------------------------------------------

def test_get_all_animals_and_filter():
    """Verify all animals are returned, and filtering by taxonomic class works."""
    # Fetch all animals
    response = client.get("/api/animals")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) >= 30

    # Filter strictly by class (Mammal)
    res_mammals = client.get("/api/animals?class=Mammal")
    assert res_mammals.status_code == 200
    mammals = res_mammals.json()
    assert len(mammals) > 0
    assert all(a["className"] == "Mammal" for a in mammals)


def test_search_animals():
    """Verify substring search returns relevant animals matching common name."""
    response = client.get("/api/search?q=tiger")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert any("tiger" in a["name"].lower() for a in results)


def test_animal_details():
    """Verify complete profile and graph relationships for an individual animal."""
    response = client.get("/api/animals/animal_tiger")
    assert response.status_code == 200
    tiger = response.json()
    assert tiger["name"] == "Tiger"
    assert tiger["species"] == "Bengal / Siberian Tiger"
    assert tiger["className"] == "Mammal"
    assert tiger["diet"] == "Carnivore"
    assert "Forest" in tiger["habitats"]
    assert "Deer" in tiger["foodSources"]
    assert "Asia" in tiger["continents"]


def test_animal_details_not_found():
    """Verify that querying a non-existent entity returns a 404 status code."""
    response = client.get("/api/animals/non_existent_animal_12345")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 3. Category Relationship Traversal Tests
# ---------------------------------------------------------------------------

def test_habitat_query():
    """Verify traversal query by habitat biome."""
    response = client.get("/api/habitats/Forest/animals")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) > 0
    assert any(a["name"] == "Tiger" for a in animals)


def test_conservation_query():
    """Verify traversal query by IUCN conservation status."""
    response = client.get("/api/conservation/Endangered/animals")
    assert response.status_code == 200
    endangered = response.json()
    assert len(endangered) > 0
    assert any(a["name"] == "Tiger" for a in endangered)


def test_diet_query():
    """Verify traversal query by dietary classification."""
    response = client.get("/api/diets/Carnivore/animals")
    assert response.status_code == 200
    carnivores = response.json()
    assert len(carnivores) > 0
    assert any(a["name"] == "Lion" for a in carnivores)


def test_continent_query():
    """Verify traversal query by geographical continent."""
    response = client.get("/api/continents/Africa/animals")
    assert response.status_code == 200
    africa_animals = response.json()
    assert len(africa_animals) > 0
    assert any(a["name"] == "Lion" for a in africa_animals)


# ---------------------------------------------------------------------------
# 4. Natural Language Cypher Engine Tests
# ---------------------------------------------------------------------------

def test_ask_knowledge_graph_endangered_forest():
    """Verify NL query parsing for multi-entity constraints (Status + Habitat)."""
    payload = {"question": "Show endangered animals that live in forests"}
    response = client.post("/api/queries/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detectedFilters"].get("status") == "Endangered"
    assert data["detectedFilters"].get("habitat") == "Forest"
    assert "MATCH" in data["cypherQuery"]
    assert "WHERE" in data["cypherQuery"]
    assert any(a["name"] == "Tiger" for a in data["results"])


def test_ask_knowledge_graph_carnivorous_mammals():
    """Verify NL query parsing for Diet + Class constraints."""
    payload = {"question": "Show carnivorous mammals"}
    response = client.post("/api/queries/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detectedFilters"].get("diet") == "Carnivore"
    assert data["detectedFilters"].get("class") == "Mammal"
    assert any(a["name"] in ["Tiger", "Lion", "Leopard", "Wolf"] for a in data["results"])


def test_ask_knowledge_graph_animals_eating_fish():
    """Verify disambiguation: 'eats fish' translates to Food constraint rather than Class."""
    payload = {"question": "Show animals that eat fish"}
    response = client.post("/api/queries/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detectedFilters"].get("food") == "Fish"
    assert any(a["name"] in ["Bald Eagle", "Brown Bear", "Saltwater Crocodile"] for a in data["results"])


# ---------------------------------------------------------------------------
# 5. Graph Visualization Topology Tests
# ---------------------------------------------------------------------------

def test_animal_graph_endpoint():
    """Verify graph payload contains typed vertices and directed edges."""
    response = client.get("/api/animals/animal_tiger/graph")
    assert response.status_code == 200
    graph = response.json()
    node_labels = [n["label"] for n in graph["nodes"]]
    rel_types = [r["type"] for r in graph["relationships"]]
    assert "Tiger" in node_labels
    assert "Forest" in node_labels
    assert "Carnivore" in node_labels
    assert "LIVES_IN" in rel_types
    assert "HAS_DIET" in rel_types
    assert "EATS" in rel_types
