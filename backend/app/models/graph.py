"""
Graph Topology and Network Visualization Models.

Defines schemas consumed by frontend graph visualizers (e.g., Vis.js, React Force Graph, Cytoscape):
- GraphNode: Graph vertex with UI-ready label, type classification, and node properties.
- GraphRelationship: Directed edge connecting source and target nodes with edge type.
- GraphResponse: Composite graph payload containing node and edge arrays.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    """
    Represents a single node (vertex) in the knowledge graph.
    """
    id: str = Field(..., description="Unique node ID in the graph (e.g. 'animal_tiger', 'habitat_forest')")
    label: str = Field(..., description="Human-readable display text on the visualization node")
    type: str = Field(..., description="Label category: Animal, Species, Class, Habitat, Diet, Food, ConservationStatus, Continent")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary key-value metadata attached to the node")


class GraphRelationship(BaseModel):
    """
    Represents a directed relationship (edge) between two nodes in the graph.
    """
    id: str = Field(..., description="Unique edge identifier")
    source: str = Field(..., description="Source node id (e.g. 'animal_tiger')")
    target: str = Field(..., description="Target node id (e.g. 'habitat_forest')")
    type: str = Field(..., description="Relationship type: BELONGS_TO_SPECIES, LIVES_IN, HAS_DIET, EATS, HAS_STATUS, FOUND_IN, etc.")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary properties on the relationship edge")


class GraphResponse(BaseModel):
    """
    Standard visualization payload containing nodes and edges for network rendering.
    """
    nodes: List[GraphNode] = Field(default_factory=list, description="Array of visual graph vertices")
    relationships: List[GraphRelationship] = Field(default_factory=list, description="Array of directed edges connecting vertices")
