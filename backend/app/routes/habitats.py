"""
Category and Relationship Queries API Router.

Provides category-based traversal endpoints for accessing fauna by single graph dimensions:
- GET /api/habitats/{habitat_name}/animals: Animals residing in a specific habitat biome.
- GET /api/conservation/{status}/animals: Animals categorized under an IUCN status.
- GET /api/diets/{diet_name}/animals: Animals possessing a specific dietary classification.
- GET /api/continents/{continent_name}/animals: Animals native to a geographical continent.
"""

from typing import List
from fastapi import APIRouter
from app.models.animal import AnimalSummary
from app.services.search_service import SearchService

router = APIRouter(tags=["Categories"])


@router.get("/api/habitats/{habitat_name}/animals", response_model=List[AnimalSummary])
def get_animals_by_habitat(habitat_name: str):
    """
    Retrieve animals living in the specified habitat.
    
    Traverses: (a:Animal)-[:LIVES_IN]->(h:Habitat {name: habitat_name})
    """
    return SearchService.get_by_habitat(habitat_name)


@router.get("/api/conservation/{status}/animals", response_model=List[AnimalSummary])
def get_animals_by_conservation(status: str):
    """
    Retrieve animals with the specified conservation status.
    
    Traverses: (a:Animal)-[:HAS_STATUS]->(cs:ConservationStatus {name: status})
    """
    return SearchService.get_by_conservation(status)


@router.get("/api/diets/{diet_name}/animals", response_model=List[AnimalSummary])
def get_animals_by_diet(diet_name: str):
    """
    Retrieve animals belonging to the specified diet category.
    
    Traverses: (a:Animal)-[:HAS_DIET]->(d:Diet {name: diet_name})
    """
    return SearchService.get_by_diet(diet_name)


@router.get("/api/continents/{continent_name}/animals", response_model=List[AnimalSummary])
def get_animals_by_continent(continent_name: str):
    """
    Retrieve animals found in the specified continent.
    
    Traverses: (a:Animal)-[:FOUND_IN]->(ct:Continent {name: continent_name})
    """
    return SearchService.get_by_continent(continent_name)
