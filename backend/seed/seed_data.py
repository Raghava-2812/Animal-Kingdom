"""
Database Seeding Script for Neo4j Knowledge Graph.

Populates a fresh or existing Neo4j database with the complete Animal Kingdom Knowledge Graph:
1. Enforces schema constraints and indexes (id uniqueness, property lookups).
2. Creates Continent, Class, Diet, and ConservationStatus reference nodes.
3. Inserts Habitat biome nodes and links them to native continents (:LOCATED_IN).
4. Inserts Animal and Species nodes with biological properties (lifespan, images, descriptions).
5. Establishes explicit graph relationships:
   - (:Animal)-[:BELONGS_TO_SPECIES]->(:Species)-[:BELONGS_TO_CLASS]->(:Class)
   - (:Animal)-[:LIVES_IN]->(:Habitat)
   - (:Animal)-[:HAS_DIET]->(:Diet)
   - (:Animal)-[:EATS]->(:Food)
   - (:Animal)-[:HAS_STATUS]->(:ConservationStatus)
   - (:Animal)-[:FOUND_IN]->(:Continent)
6. Verifies total node tallies upon completion.

Usage:
    python -m seed.seed_data           # Idempotent MERGE without deleting existing data
    python -m seed.seed_data --clear   # Wipes existing graph before re-seeding
"""

import sys
import logging
from pathlib import Path

# Add backend directory to path so imports work when executed directly from CLI
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.neo4j import neo4j_client
from app.database.schema import init_schema
from seed.animals_data import (
    CLASSES_DATA,
    DIETS_DATA,
    CONSERVATION_STATUSES_DATA,
    CONTINENTS_DATA,
    HABITATS_DATA,
    ANIMALS_DATA,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_data")


def seed_database(clear_existing: bool = False) -> bool:
    """
    Executes the multi-step seeding procedure against Neo4j.

    Args:
        clear_existing (bool): If True, executes 'MATCH (n) DETACH DELETE n;' first.

    Returns:
        bool: True if seeding succeeded, False on connection failure.
    """
    logger.info("Starting Neo4j database initialization and seeding...")

    # Ensure Neo4j connection is active
    if not neo4j_client.is_connected:
        connected = neo4j_client.connect()
        if not connected:
            logger.error("Could not connect to Neo4j database. Ensure Neo4j is running.")
            return False

    # Optional wipe of existing nodes and relationships
    if clear_existing:
        logger.warning("Clearing existing Knowledge Graph...")
        neo4j_client.execute_write("MATCH (n) DETACH DELETE n;")

    # Step 1: Ensure uniqueness constraints and search indexes
    logger.info("Step 1: Applying constraints and indexes...")
    init_schema()

    # Step 2: Seed Continent nodes (Asia, Africa, Europe, Americas, etc.)
    logger.info("Step 2: Creating Continent nodes...")
    for item in CONTINENTS_DATA:
        neo4j_client.execute_write(
            """
            MERGE (c:Continent {id: $id})
            SET c.name = $name
            """,
            {"id": item["id"], "name": item["name"]}
        )

    # Step 3: Seed Taxonomic Class nodes (Mammal, Bird, Reptile, etc.)
    logger.info("Step 3: Creating Class nodes...")
    for item in CLASSES_DATA:
        neo4j_client.execute_write(
            """
            MERGE (c:Class {id: $id})
            SET c.name = $name
            """,
            {"id": item["id"], "name": item["name"]}
        )

    # Step 4: Seed Dietary category nodes (Carnivore, Herbivore, etc.)
    logger.info("Step 4: Creating Diet nodes...")
    for item in DIETS_DATA:
        neo4j_client.execute_write(
            """
            MERGE (d:Diet {id: $id})
            SET d.name = $name
            """,
            {"id": item["id"], "name": item["name"]}
        )

    # Step 5: Seed IUCN Conservation Status nodes (Endangered, Vulnerable, etc.)
    logger.info("Step 5: Creating ConservationStatus nodes...")
    for item in CONSERVATION_STATUSES_DATA:
        neo4j_client.execute_write(
            """
            MERGE (s:ConservationStatus {id: $id})
            SET s.name = $name
            """,
            {"id": item["id"], "name": item["name"]}
        )

    # Step 6: Seed Habitat biomes and link to native continents (:LOCATED_IN)
    logger.info("Step 6: Creating Habitat nodes and Continent relationships...")
    for item in HABITATS_DATA:
        neo4j_client.execute_write(
            """
            MERGE (h:Habitat {id: $id})
            SET h.name = $name, h.description = $description
            """,
            {"id": item["id"], "name": item["name"], "description": item["description"]}
        )
        for cont_name in item["continents"]:
            neo4j_client.execute_write(
                """
                MATCH (h:Habitat {id: $hid}), (c:Continent {name: $cname})
                MERGE (h)-[:LOCATED_IN]->(c)
                """,
                {"hid": item["id"], "cname": cont_name}
            )

    # Step 7: Create Animals, Species, and all graph relationships
    logger.info("Step 7: Creating Animals, Species, and All Graph Relationships...")
    for a in ANIMALS_DATA:
        # Create Animal entity vertex
        neo4j_client.execute_write(
            """
            MERGE (an:Animal {id: $id})
            SET an.name = $name,
                an.scientificName = $scientificName,
                an.description = $description,
                an.averageLifespan = $averageLifespan,
                an.imageUrl = $imageUrl
            """,
            {
                "id": a["id"],
                "name": a["name"],
                "scientificName": a["scientificName"],
                "description": a["description"],
                "averageLifespan": a["averageLifespan"],
                "imageUrl": a.get("imageUrl", "")
            }
        )

        # Species node & Taxonomic hierarchy: Animal -> Species -> Class
        sp = a["species"]
        neo4j_client.execute_write(
            """
            MERGE (s:Species {id: $sp_id})
            SET s.name = $sp_name, s.scientificName = $sp_sci
            WITH s
            MATCH (an:Animal {id: $an_id})
            MERGE (an)-[:BELONGS_TO_SPECIES]->(s)
            WITH s
            MATCH (c:Class {name: $class_name})
            MERGE (s)-[:BELONGS_TO_CLASS]->(c)
            """,
            {
                "sp_id": sp["id"],
                "sp_name": sp["name"],
                "sp_sci": sp["scientificName"],
                "an_id": a["id"],
                "class_name": a["class"]
            }
        )

        # Diet relationship: Animal -[:HAS_DIET]-> Diet
        neo4j_client.execute_write(
            """
            MATCH (an:Animal {id: $an_id}), (d:Diet {name: $diet_name})
            MERGE (an)-[:HAS_DIET]->(d)
            """,
            {"an_id": a["id"], "diet_name": a["diet"]}
        )

        # Status relationship: Animal -[:HAS_STATUS]-> ConservationStatus
        neo4j_client.execute_write(
            """
            MATCH (an:Animal {id: $an_id}), (cs:ConservationStatus {name: $status_name})
            MERGE (an)-[:HAS_STATUS]->(cs)
            """,
            {"an_id": a["id"], "status_name": a["status"]}
        )

        # Habitat relationship: Animal -[:LIVES_IN]-> Habitat
        for hab_name in a["habitats"]:
            neo4j_client.execute_write(
                """
                MATCH (an:Animal {id: $an_id}), (h:Habitat {name: $hab_name})
                MERGE (an)-[:LIVES_IN]->(h)
                """,
                {"an_id": a["id"], "hab_name": hab_name}
            )

        # Food relationship: Animal -[:EATS]-> Food
        for food_name in a["foods"]:
            food_id = f"food_{food_name.lower().replace(' ', '_')}"
            neo4j_client.execute_write(
                """
                MERGE (f:Food {id: $f_id})
                SET f.name = $f_name
                WITH f
                MATCH (an:Animal {id: $an_id})
                MERGE (an)-[:EATS]->(f)
                """,
                {"f_id": food_id, "f_name": food_name, "an_id": a["id"]}
            )

        # Continent relationship: Animal -[:FOUND_IN]-> Continent
        for cont_name in a["continents"]:
            neo4j_client.execute_write(
                """
                MATCH (an:Animal {id: $an_id}), (c:Continent {name: $c_name})
                MERGE (an)-[:FOUND_IN]->(c)
                """,
                {"an_id": a["id"], "c_name": cont_name}
            )

    # Step 8: Verify totals in Neo4j
    logger.info("Step 8: Verifying seeded graph counts...")
    stats = neo4j_client.execute_read(
        """
        MATCH (a:Animal)
        WITH count(a) AS totalAnimals
        MATCH (s:Species)
        WITH totalAnimals, count(s) AS totalSpecies
        MATCH (h:Habitat)
        WITH totalAnimals, totalSpecies, count(h) AS totalHabitats
        MATCH (f:Food)
        WITH totalAnimals, totalSpecies, totalHabitats, count(f) AS totalFoods
        RETURN totalAnimals, totalSpecies, totalHabitats, totalFoods
        """
    )
    if stats:
        logger.info("Database verification results: %s", stats[0])
    logger.info("Knowledge Graph seeding completed successfully!")
    return True


if __name__ == "__main__":
    # Parse CLI argument for --clear
    clear = "--clear" in sys.argv
    seed_database(clear_existing=clear)
