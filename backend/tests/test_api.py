import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.query_service import QueryService

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "neo4jConnected" in data

def test_dashboard_stats():
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["totalAnimals"] >= 30
    assert data["totalSpecies"] >= 30
    assert data["totalHabitats"] >= 5
    assert data["totalEndangeredAnimals"] >= 1

def test_get_all_animals_and_filter():
    # Fetch all
    response = client.get("/api/animals")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) >= 30

    # Filter by class
    res_mammals = client.get("/api/animals?class=Mammal")
    assert res_mammals.status_code == 200
    mammals = res_mammals.json()
    assert len(mammals) > 0
    assert all(a["className"] == "Mammal" for a in mammals)

def test_search_animals():
    response = client.get("/api/search?q=tiger")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert any("tiger" in a["name"].lower() for a in results)

def test_animal_details():
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
    response = client.get("/api/animals/non_existent_animal_12345")
    assert response.status_code == 404

def test_habitat_query():
    response = client.get("/api/habitats/Forest/animals")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) > 0
    assert any(a["name"] == "Tiger" for a in animals)

def test_conservation_query():
    response = client.get("/api/conservation/Endangered/animals")
    assert response.status_code == 200
    endangered = response.json()
    assert len(endangered) > 0
    assert any(a["name"] == "Tiger" for a in endangered)

def test_diet_query():
    response = client.get("/api/diets/Carnivore/animals")
    assert response.status_code == 200
    carnivores = response.json()
    assert len(carnivores) > 0
    assert any(a["name"] == "Lion" for a in carnivores)

def test_continent_query():
    response = client.get("/api/continents/Africa/animals")
    assert response.status_code == 200
    africa_animals = response.json()
    assert len(africa_animals) > 0
    assert any(a["name"] == "Lion" for a in africa_animals)

def test_ask_knowledge_graph_endangered_forest():
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
    payload = {"question": "Show carnivorous mammals"}
    response = client.post("/api/queries/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detectedFilters"].get("diet") == "Carnivore"
    assert data["detectedFilters"].get("class") == "Mammal"
    assert any(a["name"] in ["Tiger", "Lion", "Leopard", "Wolf"] for a in data["results"])

def test_ask_knowledge_graph_animals_eating_fish():
    payload = {"question": "Show animals that eat fish"}
    response = client.post("/api/queries/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detectedFilters"].get("food") == "Fish"
    assert any(a["name"] in ["Bald Eagle", "Brown Bear", "Saltwater Crocodile"] for a in data["results"])

def test_animal_graph_endpoint():
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
