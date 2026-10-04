from typing import List
from fastapi import APIRouter, Query
from app.models.animal import AnimalSummary
from app.services.search_service import SearchService

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.get("", response_model=List[AnimalSummary])
def search_animals(q: str = Query(..., min_length=1, description="Animal name or scientific name query")):
    """Search animals by name or scientific name."""
    return SearchService.search_animals(q)
