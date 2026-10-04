from fastapi import APIRouter
from app.models.animal import DashboardStats
from app.services.animal_service import AnimalService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats():
    """Retrieve high-level Knowledge Graph statistics from Neo4j."""
    return AnimalService.get_dashboard_stats()
