import logging
from app.database.neo4j import neo4j_client

logger = logging.getLogger(__name__)

CONSTRAINTS = [
    "CREATE CONSTRAINT animal_id_unique IF NOT EXISTS FOR (a:Animal) REQUIRE a.id IS UNIQUE;",
    "CREATE CONSTRAINT species_id_unique IF NOT EXISTS FOR (s:Species) REQUIRE s.id IS UNIQUE;",
    "CREATE CONSTRAINT class_id_unique IF NOT EXISTS FOR (c:Class) REQUIRE c.id IS UNIQUE;",
    "CREATE CONSTRAINT habitat_id_unique IF NOT EXISTS FOR (h:Habitat) REQUIRE h.id IS UNIQUE;",
    "CREATE CONSTRAINT diet_id_unique IF NOT EXISTS FOR (d:Diet) REQUIRE d.id IS UNIQUE;",
    "CREATE CONSTRAINT food_id_unique IF NOT EXISTS FOR (f:Food) REQUIRE f.id IS UNIQUE;",
    "CREATE CONSTRAINT status_id_unique IF NOT EXISTS FOR (cs:ConservationStatus) REQUIRE cs.id IS UNIQUE;",
    "CREATE CONSTRAINT continent_id_unique IF NOT EXISTS FOR (ct:Continent) REQUIRE ct.id IS UNIQUE;"
]

INDEXES = [
    "CREATE INDEX animal_name_idx IF NOT EXISTS FOR (a:Animal) ON (a.name);",
    "CREATE INDEX animal_sci_name_idx IF NOT EXISTS FOR (a:Animal) ON (a.scientificName);",
    "CREATE INDEX habitat_name_idx IF NOT EXISTS FOR (h:Habitat) ON (h.name);",
    "CREATE INDEX diet_name_idx IF NOT EXISTS FOR (d:Diet) ON (d.name);",
    "CREATE INDEX status_name_idx IF NOT EXISTS FOR (cs:ConservationStatus) ON (cs.name);",
    "CREATE INDEX continent_name_idx IF NOT EXISTS FOR (ct:Continent) ON (ct.name);"
]

def init_schema() -> bool:
    """Initialize uniqueness constraints and indexes in Neo4j."""
    if not neo4j_client.is_connected:
        logger.warning("Neo4j is not connected. Skipping schema initialization.")
        return False

    try:
        for stmt in CONSTRAINTS:
            neo4j_client.execute_write(stmt)
            logger.info("Executed constraint statement: %s", stmt)

        for stmt in INDEXES:
            neo4j_client.execute_write(stmt)
            logger.info("Executed index statement: %s", stmt)

        logger.info("All constraints and indexes successfully created or verified.")
        return True
    except Exception as e:
        logger.error("Error creating schema constraints/indexes: %s", str(e))
        raise
