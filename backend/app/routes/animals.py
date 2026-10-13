"""
Animal API Router.

Exposes REST endpoints for querying Animal entities, retrieving individual
biological profiles, and obtaining subgraph visual topologies:
- GET /api/animals: Multi-facet filtered listing of animal entities.
- GET /api/animals/{animal_id}: Deep profile with taxonomic lineage, diet, and habitat.
- GET /api/animals/{animal_id}/graph: Vis.js/React-Force-Graph compatible node-and-edge network.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.animal import AnimalDetail, AnimalSummary
from app.models.graph import GraphResponse
from app.services.animal_service import AnimalService
from app.services.graph_service import GraphService

router = APIRouter(prefix="/api/animals", tags=["Animals"])


@router.get("", response_model=List[AnimalSummary])
def get_all_animals(
    class_name: Optional[str] = Query(None, alias="class", description="Taxonomic class (e.g. 'Mammal')"),
    habitat: Optional[str] = Query(None, description="Biome name (e.g. 'Forest')"),
    diet: Optional[str] = Query(None, description="Diet category (e.g. 'Carnivore')"),
    status: Optional[str] = Query(None, description="IUCN status (e.g. 'Endangered')"),
    continent: Optional[str] = Query(None, description="Continent location (e.g. 'Asia')")
):
    """
    List all animals with optional multi-facet filtering.

    All query parameters are optional and combined via logical AND.
    Returns:
        List[AnimalSummary]: Array of animal summary records.
    """
    return AnimalService.get_all_animals(
        class_name=class_name,
        habitat_name=habitat,
        diet_name=diet,
        status_name=status,
        continent_name=continent
    )


@router.get("/{animal_id}", response_model=AnimalDetail)
def get_animal_details(animal_id: str):
    """
    Retrieve comprehensive animal details and graph connections.

    Args:
        animal_id (str): Identifier of the animal entity (e.g. 'animal_tiger').

    Raises:
        HTTPException 404: If the entity ID does not exist in the graph.
    """
    animal = AnimalService.get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal with id '{animal_id}' not found.")
    return animal


@router.get("/{animal_id}/graph", response_model=GraphResponse)
def get_animal_graph(animal_id: str):
    """
    Retrieve nodes and relationships for frontend graph visualization.

    Constructs an ego-network containing the central animal entity connected
    to species, class, habitats, food sources, status, and continents.

    Args:
        animal_id (str): Identifier of the animal entity.

    Raises:
        HTTPException 404: If no graph data exists for the given ID.
    """
    subgraph = GraphService.get_animal_subgraph(animal_id)
    if not subgraph.nodes:
        raise HTTPException(status_code=404, detail=f"No graph found for animal '{animal_id}'.")
    return subgraph
