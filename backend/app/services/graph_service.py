"""
Graph Visualization Service.

Transforms knowledge graph entities into node-and-edge network topologies
formatted specifically for frontend interactive force-directed graph rendering.

Provides:
- `get_animal_subgraph`: Generates an ego-network centered around a specific animal entity,
  connecting its taxonomic species, class, habitats, diet, prey items, IUCN status, and continents.
- `get_ecosystem_subgraph`: Merges ego-networks of multiple animals into an interconnected web,
  demonstrating shared biomes, common prey, and taxonomic convergences.
"""

import logging
from typing import Dict, List, Optional, Set
from app.database.neo4j import neo4j_client
from app.models.graph import GraphNode, GraphRelationship, GraphResponse
from seed.animals_data import ANIMALS_DATA

logger = logging.getLogger(__name__)


class GraphService:
    """
    Constructs graph visual payloads with typed vertices and directed edges.
    """

    @staticmethod
    def get_animal_subgraph(animal_id: str) -> GraphResponse:
        """
        Builds a dedicated ego-network graph around an individual animal entity.

        Traverses outgoing relationships:
        1. Animal -> BELONGS_TO_SPECIES -> Species
        2. Species -> BELONGS_TO_CLASS -> Class
        3. Animal -> LIVES_IN -> Habitat
        4. Animal -> HAS_DIET -> Diet
        5. Animal -> EATS -> Food
        6. Animal -> HAS_STATUS -> ConservationStatus
        7. Animal -> FOUND_IN -> Continent

        Args:
            animal_id (str): Entity identifier (e.g., 'animal_tiger')

        Returns:
            GraphResponse: Object containing unique nodes and directed relationships.
        """
        # Find animal in seeded data dataset
        target = None
        for a in ANIMALS_DATA:
            if a["id"].lower() == animal_id.lower() or a["name"].lower().replace(" ", "_") == animal_id.lower():
                target = a
                break

        if not target:
            return GraphResponse(nodes=[], relationships=[])

        nodes: List[GraphNode] = []
        relationships: List[GraphRelationship] = []
        added_nodes: Set[str] = set()

        def add_node(nid: str, label: str, ntype: str, props: Optional[Dict] = None):
            """Helper closure to add unique graph vertices without duplication."""
            if nid not in added_nodes:
                added_nodes.add(nid)
                nodes.append(GraphNode(id=nid, label=label, type=ntype, properties=props or {}))

        # 1. Primary Animal Center Node
        add_node(
            target["id"],
            target["name"],
            "Animal",
            {
                "scientificName": target["scientificName"],
                "lifespan": target["averageLifespan"],
                "imageUrl": target.get("imageUrl", "")
            }
        )

        # 2. Species Node & BELONGS_TO_SPECIES Edge
        sp = target["species"]
        add_node(sp["id"], sp["name"], "Species", {"scientificName": sp["scientificName"]})
        relationships.append(
            GraphRelationship(
                id=f"rel_{target['id']}_species",
                source=target["id"],
                target=sp["id"],
                type="BELONGS_TO_SPECIES"
            )
        )

        # 3. Class Node & BELONGS_TO_CLASS Edge
        class_id = f"class_{target['class'].lower()}"
        add_node(class_id, target["class"], "Class")
        relationships.append(
            GraphRelationship(
                id=f"rel_{sp['id']}_class",
                source=sp["id"],
                target=class_id,
                type="BELONGS_TO_CLASS"
            )
        )

        # 4. Habitat Nodes & LIVES_IN Edges
        for hab in target["habitats"]:
            hid = f"habitat_{hab.lower().replace(' ', '_')}"
            add_node(hid, hab, "Habitat")
            relationships.append(
                GraphRelationship(
                    id=f"rel_{target['id']}_{hid}",
                    source=target["id"],
                    target=hid,
                    type="LIVES_IN"
                )
            )

        # 5. Diet Node & HAS_DIET Edge
        diet_id = f"diet_{target['diet'].lower()}"
        add_node(diet_id, target["diet"], "Diet")
        relationships.append(
            GraphRelationship(
                id=f"rel_{target['id']}_{diet_id}",
                source=target["id"],
                target=diet_id,
                type="HAS_DIET"
            )
        )

        # 6. Food Nodes & EATS Edges
        for food in target["foods"]:
            fid = f"food_{food.lower().replace(' ', '_')}"
            add_node(fid, food, "Food")
            relationships.append(
                GraphRelationship(
                    id=f"rel_{target['id']}_{fid}",
                    source=target["id"],
                    target=fid,
                    type="EATS"
                )
            )

        # 7. Conservation Status Node & HAS_STATUS Edge
        status_id = f"status_{target['status'].lower().replace(' ', '_')}"
        add_node(status_id, target["status"], "ConservationStatus")
        relationships.append(
            GraphRelationship(
                id=f"rel_{target['id']}_{status_id}",
                source=target["id"],
                target=status_id,
                type="HAS_STATUS"
            )
        )

        # 8. Continent Nodes & FOUND_IN Edges
        for cont in target["continents"]:
            cid = f"continent_{cont.lower().replace(' ', '_')}"
            add_node(cid, cont, "Continent")
            relationships.append(
                GraphRelationship(
                    id=f"rel_{target['id']}_{cid}",
                    source=target["id"],
                    target=cid,
                    type="FOUND_IN"
                )
            )

        return GraphResponse(nodes=nodes, relationships=relationships)

    @classmethod
    def get_ecosystem_subgraph(cls, limit: int = 8) -> GraphResponse:
        """
        Returns a multi-animal ecosystem subnetwork demonstrating cross-entity graph connectivity.

        Aggregates ego-networks of multiple animals, deduplicating shared entities
        such as identical habitats, shared food sources, and taxonomic classes.

        Args:
            limit (int): Number of animal clusters to include in the ecosystem view (default: 8).

        Returns:
            GraphResponse: Combined deduplicated graph topology for interactive visualization.
        """
        nodes: List[GraphNode] = []
        relationships: List[GraphRelationship] = []
        added_nodes: Set[str] = set()
        added_rel_ids: Set[str] = set()

        sample_animals = ANIMALS_DATA[:limit]

        for a in sample_animals:
            sub = cls.get_animal_subgraph(a["id"])
            for n in sub.nodes:
                if n.id not in added_nodes:
                    added_nodes.add(n.id)
                    nodes.append(n)
            for r in sub.relationships:
                if r.id not in added_rel_ids:
                    added_rel_ids.add(r.id)
                    relationships.append(r)

        return GraphResponse(nodes=nodes, relationships=relationships)
