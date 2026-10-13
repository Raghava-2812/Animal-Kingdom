"""
Dashboard API Router.

Provides aggregate system metrics and knowledge graph node tallies for the homepage dashboard:
- GET /api/dashboard/stats: High-level counts of Animals, Species, Habitats, Foods, and Endangered species.
"""

from fastapi import APIRouter
from app.models.animal import DashboardStats
from app.services.animal_service import AnimalService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats():
    """
    Retrieve high-level Knowledge Graph statistics from Neo4j.

    Executes aggregation queries across all core labels to produce metrics
    for the frontend analytics cards and dashboard widgets.
    """
    return AnimalService.get_dashboard_stats()
