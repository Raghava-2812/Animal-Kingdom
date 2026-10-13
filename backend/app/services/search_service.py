"""
Faceted Entity Search Service.

Handles targeted keyword and category search operations across graph dimensions:
- Text substring search across animal common names, scientific binomials, and species names.
- Traversal queries filtering entities by Habitat biome, IUCN status, Dietary habit, and Continents.

Features transparent in-memory fallbacks to `ANIMALS_DATA` if the Neo4j database is offline.
"""

import logging
from typing import List
from app.database.neo4j import neo4j_client
from app.models.animal import AnimalSummary
from seed.animals_data import ANIMALS_DATA

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service layer providing specialized graph queries for search and category filtering.
    """

    @staticmethod
    def search_animals(query: str) -> List[AnimalSummary]:
        """
        Searches animals by freeform text across name, scientific name, and taxonomy.

        Cypher Traversal:
        - Matches (a:Animal) where lowercase name or scientific name contains the search term.
        - Expands taxonomy, biomes, status, diet, and continents using OPTIONAL MATCH.

        Args:
            query (str): Search keyword or partial string.

        Returns:
            List[AnimalSummary]: Matched animals sorted alphabetically.
        """
        if not query or not query.strip():
            return []

        q = query.strip()

        if neo4j_client.is_connected:
            try:
                cypher = """
                MATCH (a:Animal)
                WHERE toLower(a.name) CONTAINS toLower($q)
                   OR toLower(a.scientificName) CONTAINS toLower($q)
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
                OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
                OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
                OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
                RETURN a.id AS id,
                       a.name AS name,
                       a.scientificName AS scientificName,
                       a.description AS description,
                       a.averageLifespan AS averageLifespan,
                       a.imageUrl AS imageUrl,
                       c.name AS className,
                       cs.name AS conservationStatus,
                       d.name AS diet,
                       collect(DISTINCT h.name) AS habitats,
                       collect(DISTINCT ct.name) AS continents
                ORDER BY a.name
                """
                results = neo4j_client.execute_read(cypher, {"q": q})
                return [AnimalSummary(**row) for row in results]
            except Exception as e:
                logger.error("Failed to execute animal search on Neo4j: %s", str(e))

        # Fallback: In-memory substring search over static dataset
        results = []
        q_lower = q.lower()
        for a in ANIMALS_DATA:
            if (
                q_lower in a["name"].lower()
                or q_lower in a["scientificName"].lower()
                or q_lower in a["species"]["name"].lower()
            ):
                results.append(
                    AnimalSummary(
                        id=a["id"],
                        name=a["name"],
                        scientificName=a["scientificName"],
                        description=a["description"],
                        averageLifespan=a["averageLifespan"],
                        imageUrl=a.get("imageUrl"),
                        className=a["class"],
                        conservationStatus=a["status"],
                        diet=a["diet"],
                        habitats=a["habitats"],
                        continents=a["continents"]
                    )
                )
        return sorted(results, key=lambda x: x.name)

    @staticmethod
    def get_by_habitat(habitat_name: str) -> List[AnimalSummary]:
        """
        Finds all animal entities inhabiting a specific biome (e.g. 'Ocean', 'Forest').

        Graph Relationship:
        (a:Animal)-[:LIVES_IN]->(h:Habitat {name: $habitat_name})

        Args:
            habitat_name (str): Name of the habitat.

        Returns:
            List[AnimalSummary]: Animals living in the specified habitat.
        """
        if neo4j_client.is_connected:
            try:
                cypher = """
                MATCH (a:Animal)-[:LIVES_IN]->(h:Habitat)
                WHERE toLower(h.name) = toLower($habitat_name)
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
                OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
                OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
                RETURN a.id AS id,
                       a.name AS name,
                       a.scientificName AS scientificName,
                       a.description AS description,
                       a.averageLifespan AS averageLifespan,
                       a.imageUrl AS imageUrl,
                       c.name AS className,
                       cs.name AS conservationStatus,
                       d.name AS diet,
                       collect(DISTINCT h.name) AS habitats,
                       collect(DISTINCT ct.name) AS continents
                ORDER BY a.name
                """
                results = neo4j_client.execute_read(cypher, {"habitat_name": habitat_name})
                return [AnimalSummary(**row) for row in results]
            except Exception as e:
                logger.error("Failed to query animals by habitat on Neo4j: %s", str(e))

        # Fallback: In-memory filter over ANIMALS_DATA
        results = []
        for a in ANIMALS_DATA:
            if any(h.lower() == habitat_name.lower() for h in a["habitats"]):
                results.append(
                    AnimalSummary(
                        id=a["id"],
                        name=a["name"],
                        scientificName=a["scientificName"],
                        description=a["description"],
                        averageLifespan=a["averageLifespan"],
                        imageUrl=a.get("imageUrl"),
                        className=a["class"],
                        conservationStatus=a["status"],
                        diet=a["diet"],
                        habitats=a["habitats"],
                        continents=a["continents"]
                    )
                )
        return sorted(results, key=lambda x: x.name)

    @staticmethod
    def get_by_conservation(status: str) -> List[AnimalSummary]:
        """
        Finds all animal entities carrying a specific IUCN conservation status.

        Graph Relationship:
        (a:Animal)-[:HAS_STATUS]->(cs:ConservationStatus {name: $status})

        Args:
            status (str): Conservation status (e.g. 'Endangered', 'Vulnerable').

        Returns:
            List[AnimalSummary]: Animals with the matching conservation status.
        """
        if neo4j_client.is_connected:
            try:
                cypher = """
                MATCH (a:Animal)-[:HAS_STATUS]->(cs:ConservationStatus)
                WHERE toLower(cs.name) = toLower($status)
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
                OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
                OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
                RETURN a.id AS id,
                       a.name AS name,
                       a.scientificName AS scientificName,
                       a.description AS description,
                       a.averageLifespan AS averageLifespan,
                       a.imageUrl AS imageUrl,
                       c.name AS className,
                       cs.name AS conservationStatus,
                       d.name AS diet,
                       collect(DISTINCT h.name) AS habitats,
                       collect(DISTINCT ct.name) AS continents
                ORDER BY a.name
                """
                results = neo4j_client.execute_read(cypher, {"status": status})
                return [AnimalSummary(**row) for row in results]
            except Exception as e:
                logger.error("Failed to query animals by conservation on Neo4j: %s", str(e))

        # Fallback: In-memory filter over ANIMALS_DATA
        results = []
        for a in ANIMALS_DATA:
            if a["status"].lower() == status.lower():
                results.append(
                    AnimalSummary(
                        id=a["id"],
                        name=a["name"],
                        scientificName=a["scientificName"],
                        description=a["description"],
                        averageLifespan=a["averageLifespan"],
                        imageUrl=a.get("imageUrl"),
                        className=a["class"],
                        conservationStatus=a["status"],
                        diet=a["diet"],
                        habitats=a["habitats"],
                        continents=a["continents"]
                    )
                )
        return sorted(results, key=lambda x: x.name)

    @staticmethod
    def get_by_diet(diet_name: str) -> List[AnimalSummary]:
        """
        Finds all animal entities belonging to a dietary category (e.g. 'Carnivore', 'Herbivore').

        Graph Relationship:
        (a:Animal)-[:HAS_DIET]->(d:Diet {name: $diet_name})

        Args:
            diet_name (str): Dietary classification.

        Returns:
            List[AnimalSummary]: Animals with the matching diet.
        """
        if neo4j_client.is_connected:
            try:
                cypher = """
                MATCH (a:Animal)-[:HAS_DIET]->(d:Diet)
                WHERE toLower(d.name) = toLower($diet_name)
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
                OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
                OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
                RETURN a.id AS id,
                       a.name AS name,
                       a.scientificName AS scientificName,
                       a.description AS description,
                       a.averageLifespan AS averageLifespan,
                       a.imageUrl AS imageUrl,
                       c.name AS className,
                       cs.name AS conservationStatus,
                       d.name AS diet,
                       collect(DISTINCT h.name) AS habitats,
                       collect(DISTINCT ct.name) AS continents
                ORDER BY a.name
                """
                results = neo4j_client.execute_read(cypher, {"diet_name": diet_name})
                return [AnimalSummary(**row) for row in results]
            except Exception as e:
                logger.error("Failed to query animals by diet on Neo4j: %s", str(e))

        # Fallback: In-memory filter over ANIMALS_DATA
        results = []
        for a in ANIMALS_DATA:
            if a["diet"].lower() == diet_name.lower():
                results.append(
                    AnimalSummary(
                        id=a["id"],
                        name=a["name"],
                        scientificName=a["scientificName"],
                        description=a["description"],
                        averageLifespan=a["averageLifespan"],
                        imageUrl=a.get("imageUrl"),
                        className=a["class"],
                        conservationStatus=a["status"],
                        diet=a["diet"],
                        habitats=a["habitats"],
                        continents=a["continents"]
                    )
                )
        return sorted(results, key=lambda x: x.name)

    @staticmethod
    def get_by_continent(continent_name: str) -> List[AnimalSummary]:
        """
        Finds all animal entities native to a geographical continent.

        Graph Relationship:
        (a:Animal)-[:FOUND_IN]->(ct:Continent {name: $continent_name})

        Args:
            continent_name (str): Continent name (e.g. 'Asia', 'Africa').

        Returns:
            List[AnimalSummary]: Animals found on the continent.
        """
        if neo4j_client.is_connected:
            try:
                cypher = """
                MATCH (a:Animal)-[:FOUND_IN]->(ct:Continent)
                WHERE toLower(ct.name) = toLower($continent_name)
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
                OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
                OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
                RETURN a.id AS id,
                       a.name AS name,
                       a.scientificName AS scientificName,
                       a.description AS description,
                       a.averageLifespan AS averageLifespan,
                       a.imageUrl AS imageUrl,
                       c.name AS className,
                       cs.name AS conservationStatus,
                       d.name AS diet,
                       collect(DISTINCT h.name) AS habitats,
                       collect(DISTINCT ct.name) AS continents
                ORDER BY a.name
                """
                results = neo4j_client.execute_read(cypher, {"continent_name": continent_name})
                return [AnimalSummary(**row) for row in results]
            except Exception as e:
                logger.error("Failed to query animals by continent on Neo4j: %s", str(e))

        # Fallback: In-memory filter over ANIMALS_DATA
        results = []
        for a in ANIMALS_DATA:
            if any(c.lower() == continent_name.lower() for c in a["continents"]):
                results.append(
                    AnimalSummary(
                        id=a["id"],
                        name=a["name"],
                        scientificName=a["scientificName"],
                        description=a["description"],
                        averageLifespan=a["averageLifespan"],
                        imageUrl=a.get("imageUrl"),
                        className=a["class"],
                        conservationStatus=a["status"],
                        diet=a["diet"],
                        habitats=a["habitats"],
                        continents=a["continents"]
                    )
                )
        return sorted(results, key=lambda x: x.name)
