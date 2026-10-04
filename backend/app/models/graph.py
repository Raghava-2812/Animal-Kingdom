from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # Animal, Species, Class, Habitat, Diet, Food, ConservationStatus, Continent
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphRelationship(BaseModel):
    id: str
    source: str
    target: str
    type: str  # BELONGS_TO_SPECIES, BELONGS_TO_CLASS, LIVES_IN, HAS_DIET, EATS, HAS_STATUS, FOUND_IN, LOCATED_IN
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    relationships: List[GraphRelationship]
