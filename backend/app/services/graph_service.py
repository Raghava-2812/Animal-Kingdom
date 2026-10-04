import logging
from typing import Dict, List, Optional, Set
from app.database.neo4j import neo4j_client
from app.models.graph import GraphNode, GraphRelationship, GraphResponse
from seed.animals_data import ANIMALS_DATA

logger = logging.getLogger(__name__)

class GraphService:
    @staticmethod
    def get_animal_subgraph(animal_id: str) -> GraphResponse:
        """Extract graph nodes and relationships for a specific animal."""
        # Find animal in memory or database
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
            if nid not in added_nodes:
                added_nodes.add(nid)
                nodes.append(GraphNode(id=nid, label=label, type=ntype, properties=props or {}))

        # 1. Animal Center Node
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

        # 2. Species Node
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

        # 3. Class Node
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

        # 4. Habitats
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

        # 5. Diet
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

        # 6. Food items
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

        # 7. Conservation Status
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

        # 8. Continents
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
        """Returns an interconnected multi-animal subnetwork demonstrating graph traversal."""
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
