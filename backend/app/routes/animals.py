from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.animal import AnimalDetail, AnimalSummary
from app.models.graph import GraphResponse
from app.services.animal_service import AnimalService
from app.services.graph_service import GraphService

router = APIRouter(prefix="/api/animals", tags=["Animals"])

@router.get("", response_model=List[AnimalSummary])
def get_all_animals(
    class_name: Optional[str] = Query(None, alias="class"),
    habitat: Optional[str] = Query(None),
    diet: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    continent: Optional[str] = Query(None)
):
    """List all animals with optional multi-facet filtering."""
    return AnimalService.get_all_animals(
        class_name=class_name,
        habitat_name=habitat,
        diet_name=diet,
        status_name=status,
        continent_name=continent
    )

@router.get("/{animal_id}", response_model=AnimalDetail)
def get_animal_details(animal_id: str):
    """Retrieve comprehensive animal details and graph connections."""
    animal = AnimalService.get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal with id '{animal_id}' not found.")
    return animal

@router.get("/{animal_id}/graph", response_model=GraphResponse)
def get_animal_graph(animal_id: str):
    """Retrieve nodes and relationships for frontend graph visualization."""
    subgraph = GraphService.get_animal_subgraph(animal_id)
    if not subgraph.nodes:
        raise HTTPException(status_code=404, detail=f"No graph found for animal '{animal_id}'.")
    return subgraph
