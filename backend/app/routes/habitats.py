from typing import List
from fastapi import APIRouter
from app.models.animal import AnimalSummary
from app.services.search_service import SearchService

router = APIRouter(tags=["Categories"])

@router.get("/api/habitats/{habitat_name}/animals", response_model=List[AnimalSummary])
def get_animals_by_habitat(habitat_name: str):
    """Retrieve animals living in the specified habitat."""
    return SearchService.get_by_habitat(habitat_name)

@router.get("/api/conservation/{status}/animals", response_model=List[AnimalSummary])
def get_animals_by_conservation(status: str):
    """Retrieve animals with the specified conservation status."""
    return SearchService.get_by_conservation(status)

@router.get("/api/diets/{diet_name}/animals", response_model=List[AnimalSummary])
def get_animals_by_diet(diet_name: str):
    """Retrieve animals belonging to the specified diet category."""
    return SearchService.get_by_diet(diet_name)

@router.get("/api/continents/{continent_name}/animals", response_model=List[AnimalSummary])
def get_animals_by_continent(continent_name: str):
    """Retrieve animals found in the specified continent."""
    return SearchService.get_by_continent(continent_name)
