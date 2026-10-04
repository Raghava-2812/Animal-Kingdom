from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.models.animal import AnimalSummary

class NaturalLanguageQueryRequest(BaseModel):
    question: str

class NaturalLanguageQueryResponse(BaseModel):
    question: str
    detectedFilters: Dict[str, Any] = Field(default_factory=dict)
    cypherQuery: str
    results: List[AnimalSummary] = Field(default_factory=list)
    resultCount: int
    explanation: Optional[str] = None
