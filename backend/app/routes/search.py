"""
Search API Router.

Provides fast text-based search endpoints:
- GET /api/search?q={query}: Substring matching against common and scientific animal names.
"""

from typing import List
from fastapi import APIRouter, Query
from app.models.animal import AnimalSummary
from app.services.search_service import SearchService

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("", response_model=List[AnimalSummary])
def search_animals(
    q: str = Query(..., min_length=1, description="Animal name or scientific name query string")
):
    """
    Search animals by common name, scientific name, or species name.

    Performs case-insensitive substring search and expands full graph context
    (taxonomy, biomes, IUCN status, diet) for each matched entity.
    """
    return SearchService.search_animals(q)
