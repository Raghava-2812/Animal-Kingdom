import logging
from typing import List, Optional
from app.database.neo4j import neo4j_client
from app.models.animal import AnimalDetail, AnimalSummary, DashboardStats
from seed.animals_data import ANIMALS_DATA, HABITATS_DATA, CONTINENTS_DATA, DIETS_DATA, CLASSES_DATA

logger = logging.getLogger(__name__)

class AnimalService:
    @staticmethod
    def get_dashboard_stats() -> DashboardStats:
        """Calculate dashboard statistics directly from Neo4j, or fallback if offline."""
        if neo4j_client.is_connected:
            try:
                query = """
                MATCH (a:Animal)
                WITH count(a) AS totalAnimals
                MATCH (s:Species)
                WITH totalAnimals, count(s) AS totalSpecies
                MATCH (h:Habitat)
                WITH totalAnimals, totalSpecies, count(h) AS totalHabitats
                MATCH (f:Food)
                WITH totalAnimals, totalSpecies, totalHabitats, count(f) AS totalFoods
                MATCH (c:Continent)
                WITH totalAnimals, totalSpecies, totalHabitats, totalFoods, count(c) AS totalContinents
                OPTIONAL MATCH (ea:Animal)-[:HAS_STATUS]->(st:ConservationStatus)
                WHERE st.name IN ["Endangered", "Critically Endangered"]
                RETURN totalAnimals, totalSpecies, totalHabitats, totalFoods, totalContinents, count(DISTINCT ea) AS totalEndangeredAnimals
                """
                results = neo4j_client.execute_read(query)
                if results:
                    row = results[0]
                    return DashboardStats(
                        totalAnimals=row["totalAnimals"],
                        totalSpecies=row["totalSpecies"],
                        totalHabitats=row["totalHabitats"],
                        totalFoods=row["totalFoods"],
                        totalEndangeredAnimals=row["totalEndangeredAnimals"],
                        totalContinents=row["totalContinents"],
                        neo4jConnected=True
                    )
            except Exception as e:
                logger.error("Failed to query Neo4j dashboard stats: %s", str(e))

        # In-memory dataset statistics fallback
        all_foods = set()
        for a in ANIMALS_DATA:
            all_foods.update(a.get("foods", []))
        endangered_count = sum(1 for a in ANIMALS_DATA if a.get("status") in ["Endangered", "Critically Endangered"])

        return DashboardStats(
            totalAnimals=len(ANIMALS_DATA),
            totalSpecies=len(ANIMALS_DATA),
            totalHabitats=len(HABITATS_DATA),
            totalFoods=len(all_foods),
            totalEndangeredAnimals=endangered_count,
            totalContinents=len(CONTINENTS_DATA),
            neo4jConnected=False
        )

    @staticmethod
    def get_all_animals(
        class_name: Optional[str] = None,
        habitat_name: Optional[str] = None,
        diet_name: Optional[str] = None,
        status_name: Optional[str] = None,
        continent_name: Optional[str] = None
    ) -> List[AnimalSummary]:
        """Fetch all animals with optional multi-facet filtering."""
        if neo4j_client.is_connected:
            try:
                match_clauses = ["(a:Animal)"]
                where_clauses = []
                params = {}

                if class_name:
                    match_clauses.append("(a)-[:BELONGS_TO_SPECIES]->(:Species)-[:BELONGS_TO_CLASS]->(fc:Class)")
                    where_clauses.append("toLower(fc.name) = toLower($class_name)")
                    params["class_name"] = class_name
                if habitat_name:
                    match_clauses.append("(a)-[:LIVES_IN]->(fh:Habitat)")
                    where_clauses.append("toLower(fh.name) = toLower($habitat_name)")
                    params["habitat_name"] = habitat_name
                if diet_name:
                    match_clauses.append("(a)-[:HAS_DIET]->(fd:Diet)")
                    where_clauses.append("toLower(fd.name) = toLower($diet_name)")
                    params["diet_name"] = diet_name
                if status_name:
                    match_clauses.append("(a)-[:HAS_STATUS]->(fcs:ConservationStatus)")
                    where_clauses.append("toLower(fcs.name) = toLower($status_name)")
                    params["status_name"] = status_name
                if continent_name:
                    match_clauses.append("(a)-[:FOUND_IN]->(fct:Continent)")
                    where_clauses.append("toLower(fct.name) = toLower($continent_name)")
                    params["continent_name"] = continent_name

                matches_str = ",\n                     ".join(match_clauses)
                where_stmt = ("\n                WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

                query = f"""
                MATCH {matches_str}{where_stmt}
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
                OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
                OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
                OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
                RETURN DISTINCT a.id AS id,
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
                results = neo4j_client.execute_read(query, params)
                return [AnimalSummary(**row) for row in results]
            except Exception as e:
                logger.error("Failed to fetch animals from Neo4j: %s", str(e))

        # In-memory fallback
        summaries = []
        for a in ANIMALS_DATA:
            if class_name and a["class"].lower() != class_name.lower():
                continue
            if habitat_name and not any(h.lower() == habitat_name.lower() for h in a["habitats"]):
                continue
            if diet_name and a["diet"].lower() != diet_name.lower():
                continue
            if status_name and a["status"].lower() != status_name.lower():
                continue
            if continent_name and not any(c.lower() == continent_name.lower() for c in a["continents"]):
                continue

            summaries.append(
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
        return sorted(summaries, key=lambda x: x.name)

    @staticmethod
    def get_animal_by_id(animal_id: str) -> Optional[AnimalDetail]:
        """Fetch detailed animal data including all graph relationships."""
        if neo4j_client.is_connected:
            try:
                query = """
                MATCH (a:Animal {id: $animal_id})
                OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(s:Species)
                OPTIONAL MATCH (s)-[:BELONGS_TO_CLASS]->(c:Class)
                OPTIONAL MATCH (a)-[:HAS_STATUS]->(cs:ConservationStatus)
                OPTIONAL MATCH (a)-[:HAS_DIET]->(d:Diet)
                OPTIONAL MATCH (a)-[:LIVES_IN]->(h:Habitat)
                OPTIONAL MATCH (a)-[:EATS]->(f:Food)
                OPTIONAL MATCH (a)-[:FOUND_IN]->(ct:Continent)
                RETURN a.id AS id,
                       a.name AS name,
                       a.scientificName AS scientificName,
                       a.description AS description,
                       a.averageLifespan AS averageLifespan,
                       a.imageUrl AS imageUrl,
                       s.name AS species,
                       s.scientificName AS speciesScientificName,
                       c.name AS className,
                       d.name AS diet,
                       cs.name AS conservationStatus,
                       collect(DISTINCT h.name) AS habitats,
                       collect(DISTINCT f.name) AS foodSources,
                       collect(DISTINCT ct.name) AS continents
                """
                results = neo4j_client.execute_read(query, {"animal_id": animal_id})
                if results and results[0]["id"] is not None:
                    return AnimalDetail(**results[0])
            except Exception as e:
                logger.error("Failed to fetch animal details from Neo4j: %s", str(e))

        # In-memory fallback
        for a in ANIMALS_DATA:
            if a["id"].lower() == animal_id.lower() or a["name"].lower().replace(" ", "_") == animal_id.lower():
                return AnimalDetail(
                    id=a["id"],
                    name=a["name"],
                    scientificName=a["scientificName"],
                    description=a["description"],
                    averageLifespan=a["averageLifespan"],
                    imageUrl=a.get("imageUrl"),
                    species=a["species"]["name"],
                    speciesScientificName=a["species"]["scientificName"],
                    className=a["class"],
                    diet=a["diet"],
                    conservationStatus=a["status"],
                    habitats=a["habitats"],
                    foodSources=a["foods"],
                    continents=a["continents"]
                )
        return None
