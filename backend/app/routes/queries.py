from typing import List
from fastapi import APIRouter
from app.models.query import NaturalLanguageQueryRequest, NaturalLanguageQueryResponse
from app.services.query_service import QueryService

router = APIRouter(prefix="/api/queries", tags=["Knowledge Graph Queries"])

EXAMPLE_QUESTIONS = [
    "Show endangered animals that live in forests",
    "Show carnivorous mammals",
    "Show herbivores found in Asia",
    "Show animals that eat fish",
    "Show animals living in grasslands",
    "Show critically endangered animals",
    "Show mammals found in Africa",
    "Show animals that live in both forests and grasslands",
    "Show animals that eat fruits",
    "Show animals found in Asia and having an endangered status"
]

@router.get("/examples", response_model=List[str])
def get_example_questions():
    """Retrieve predefined natural language questions supported by the Knowledge Graph."""
    return EXAMPLE_QUESTIONS

@router.post("/ask", response_model=NaturalLanguageQueryResponse)
def ask_knowledge_graph(request: NaturalLanguageQueryRequest):
    """Process natural language question into safe Cypher and execute."""
    return QueryService.execute_natural_language_query(request.question)
