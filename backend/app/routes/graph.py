"""
Graph Visualization API Router.

Serves network payloads formatted for interactive canvas/SVG rendering engines:
- GET /api/graph/sample: Multi-animal ecosystem network illustrating shared nodes and biomes.
- GET /api/graph/animal/{animal_id}: Ego-network for an individual animal entity.
"""

from fastapi import APIRouter, HTTPException
from app.models.graph import GraphResponse
from app.services.graph_service import GraphService

router = APIRouter(prefix="/api/graph", tags=["Graph Visualization"])


@router.get("/sample", response_model=GraphResponse)
def get_sample_graph():
    """
    Retrieve an interconnected multi-animal subnetwork for interactive exploration.

    Aggregates relationships for a representative sample of animals across multiple
    classes and habitats, showcasing cross-species links and food webs.
    """
    return GraphService.get_ecosystem_subgraph(limit=8)


@router.get("/animal/{animal_id}", response_model=GraphResponse)
def get_animal_graph(animal_id: str):
    """
    Retrieve graph visualization for an individual animal.

    Args:
        animal_id (str): Unique entity ID of the animal.

    Raises:
        HTTPException 404: If the requested animal entity does not exist.
    """
    res = GraphService.get_animal_subgraph(animal_id)
    if not res.nodes:
        raise HTTPException(status_code=404, detail=f"Animal '{animal_id}' not found.")
    return res
