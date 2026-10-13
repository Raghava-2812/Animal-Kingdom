"""
Natural Language to Cypher Query Engine Service.

Translates free-form English questions into mathematically sound, parameterized
Cypher queries executed directly against the Neo4j Knowledge Graph.

Core Functionality:
1. Entity Extraction: Extracts entity mentions for Status, Habitat, Diet, Class,
   Food/Prey, and Geographic Continent using regex dictionaries and synonyms.
2. Context Disambiguation: Differentiates between 'eats fish' (Food entity filter)
   vs. 'is a fish' (Taxonomic Class filter), and parses collective categories like
   'water/aquatic' into biomes [Ocean, River, Wetland].
3. Parameterized Cypher Compilation: Generates structured MATCH...WHERE...RETURN statements.
4. Execution & Explanation: Executes the query via Neo4j Driver and returns
   matched Animal entities along with human-readable traversal explanations.
"""

import re
import logging
from typing import Any, Dict, List, Tuple
from app.database.neo4j import neo4j_client
from app.models.animal import AnimalSummary
from app.models.query import NaturalLanguageQueryResponse
from seed.animals_data import (
    ANIMALS_DATA,
    HABITATS_DATA,
    CONTINENTS_DATA,
    DIETS_DATA,
    CLASSES_DATA,
    CONSERVATION_STATUSES_DATA,
)

logger = logging.getLogger(__name__)

# ============================================================================
# Canonical Synonym & Keyword Dictionaries
# Maps colloquial user phrases and plurals to canonical Knowledge Graph nodes
# ============================================================================

# Habitat canonical mapping (e.g., 'jungles' -> 'Forest', 'swamps' -> 'Wetland')
HABITAT_KEYWORDS = {h["name"].lower(): h["name"] for h in HABITATS_DATA}
HABITAT_KEYWORDS.update({
    "forests": "Forest",
    "forest": "Forest",
    "jungle": "Forest",
    "jungles": "Forest",
    "rainforest": "Forest",
    "rainforests": "Forest",
    "woods": "Forest",
    "woodland": "Forest",
    "grasslands": "Grassland",
    "grassland": "Grassland",
    "plains": "Grassland",
    "prairie": "Grassland",
    "savannas": "Savanna",
    "savannah": "Savanna",
    "savannahs": "Savanna",
    "savanna": "Savanna",
    "deserts": "Desert",
    "desert": "Desert",
    "oceans": "Ocean",
    "ocean": "Ocean",
    "sea": "Ocean",
    "seas": "Ocean",
    "marine": "Ocean",
    "rivers": "River",
    "river": "River",
    "stream": "River",
    "freshwater": "River",
    "wetlands": "Wetland",
    "wetland": "Wetland",
    "swamps": "Wetland",
    "swamp": "Wetland",
    "marsh": "Wetland",
    "marshes": "Wetland",
    "mountains": "Mountain",
    "mountain": "Mountain",
    "alpine": "Mountain",
    "polar": "Polar Tundra",
    "tundra": "Polar Tundra",
    "arctic": "Polar Tundra",
    "ice": "Polar Tundra",
})

# Dietary category canonical mapping (e.g., 'predator' -> 'Carnivore')
DIET_KEYWORDS = {
    "carnivore": "Carnivore",
    "carnivores": "Carnivore",
    "carnivorous": "Carnivore",
    "predator": "Carnivore",
    "predators": "Carnivore",
    "meat eater": "Carnivore",
    "meat eaters": "Carnivore",
    "meat-eater": "Carnivore",
    "meat-eaters": "Carnivore",
    "herbivore": "Herbivore",
    "herbivores": "Herbivore",
    "herbivorous": "Herbivore",
    "plant eater": "Herbivore",
    "plant eaters": "Herbivore",
    "plant-eater": "Herbivore",
    "plant-eaters": "Herbivore",
    "vegetarian": "Herbivore",
    "omnivore": "Omnivore",
    "omnivores": "Omnivore",
    "omnivorous": "Omnivore",
    "insectivore": "Insectivore",
    "insectivores": "Insectivore",
    "insectivorous": "Insectivore",
    "insect eater": "Insectivore",
    "insect eaters": "Insectivore",
}

# Taxonomic Class canonical mapping (e.g., 'avian' -> 'Bird')
CLASS_KEYWORDS = {
    "mammal": "Mammal",
    "mammals": "Mammal",
    "bird": "Bird",
    "birds": "Bird",
    "avian": "Bird",
    "reptile": "Reptile",
    "reptiles": "Reptile",
    "amphibian": "Amphibian",
    "amphibians": "Amphibian",
    "fish": "Fish",
    "fishes": "Fish",
    "insect": "Insect",
    "insects": "Insect",
    "bug": "Insect",
    "bugs": "Insect",
}

# IUCN Conservation Status mapping
STATUS_KEYWORDS = {
    "critically endangered": "Critically Endangered",
    "endangered": "Endangered",
    "vulnerable": "Vulnerable",
    "near threatened": "Near Threatened",
    "least concern": "Least Concern"
}

# Geographic Continent mapping
CONTINENT_KEYWORDS = {c["name"].lower(): c["name"] for c in CONTINENTS_DATA}
CONTINENT_KEYWORDS.update({
    "asia": "Asia",
    "africa": "Africa",
    "europe": "Europe",
    "north america": "North America",
    "south america": "South America",
    "australia": "Australia",
    "antarctica": "Antarctica"
})

# Prey & Food source mapping (e.g., 'bamboo', 'krill', 'berries')
FOOD_KEYWORDS = {
    "fish": "Fish",
    "fishes": "Fish",
    "fruit": "Fruits",
    "fruits": "Fruits",
    "grass": "Grass",
    "leaves": "Leaves",
    "leaf": "Leaves",
    "bamboo": "Bamboo",
    "deer": "Deer",
    "insects": "Insects",
    "insect": "Insects",
    "seeds": "Seeds",
    "seed": "Seeds",
    "rodents": "Rodents",
    "seals": "Seals",
    "squid": "Squid",
    "crustaceans": "Crustaceans",
    "crabs": "Crustaceans",
    "berries": "Berries",
    "eucalyptus": "Eucalyptus",
    "krill": "Krill",
    "plankton": "Plankton",
    "algae": "Algae",
    "crickets": "Crickets",
    "moths": "Moths",
}


class QueryService:
    """
    Service responsible for parsing natural-language questions and compiling Cypher queries.
    """

    @staticmethod
    def parse_natural_language_question(question: str) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        """
        Parses a natural-language question into graph entity constraints and compiles a Cypher query.

        Algorithm:
        1. Normalizes input text to lowercase.
        2. Scans for Conservation Status (matching 'critically endangered' before 'endangered').
        3. Identifies habitat biomes, parsing collective keywords like 'water/aquatic' into [Ocean, River, Wetland].
        4. Identifies dietary class, handling phrasings such as 'eat meat' -> Carnivore.
        5. Detects taxonomic class, ensuring it is not the object of an 'eat/eating' action.
        6. Extracts continents and specific food/prey items.
        7. Dynamically synthesizes parameterized Cypher query with safe MATCH and WHERE clauses.

        Args:
            question (str): The natural language query submitted by the user.

        Returns:
            Tuple[Dict[str, Any], str, Dict[str, Any]]:
                - detected_filters: Dict of identified constraint keys and values.
                - cypher_query: Complete Cypher query string ready for execution.
                - parameters: Parameter dictionary bound to the Cypher execution.
        """
        q = question.lower()
        filters: Dict[str, Any] = {}
        params: Dict[str, Any] = {}

        # ---------------------------------------------------------
        # 1. Detect Conservation Status
        # ---------------------------------------------------------
        # Evaluates 'critically endangered' before 'endangered' to avoid prefix collisions
        for term, canonical in STATUS_KEYWORDS.items():
            if re.search(r'\b' + re.escape(term) + r'\b', q):
                filters["status"] = canonical
                params["status_name"] = canonical
                break

        # ---------------------------------------------------------
        # 2. Detect Habitat Biomes
        # ---------------------------------------------------------
        # Disambiguates collective terms 'water/aquatic' and 'land/terrestrial'
        is_water_query = bool(re.search(r'\b(water|aquatic)\b', q))
        is_land_query = bool(re.search(r'\b(land|terrestrial)\b', q))

        if is_water_query:
            filters["habitat"] = "Water (Ocean / River / Wetland)"
            params["water_habitats"] = ["Ocean", "River", "Wetland"]
        elif is_land_query:
            filters["habitat"] = "Land (Forest / Grassland / Savanna / Desert / Mountain)"
            params["land_habitats"] = ["Forest", "Grassland", "Savanna", "Desert", "Mountain"]
        else:
            detected_habitats = []
            for term, canonical in HABITAT_KEYWORDS.items():
                if re.search(r'\b' + re.escape(term) + r'\b', q):
                    if canonical not in detected_habitats:
                        detected_habitats.append(canonical)
            if len(detected_habitats) == 1:
                filters["habitat"] = detected_habitats[0]
                params["habitat_name"] = detected_habitats[0]
            elif len(detected_habitats) > 1:
                # Intersecting habitats (e.g. 'both forests and grasslands')
                filters["habitats"] = detected_habitats
                params["habitat_names"] = detected_habitats

        # ---------------------------------------------------------
        # 3. Detect Diet
        # ---------------------------------------------------------
        for term, canonical in DIET_KEYWORDS.items():
            if re.search(r'\b' + re.escape(term) + r'\b', q):
                filters["diet"] = canonical
                params["diet_name"] = canonical
                break

        # Special natural language phrasings: "eat meat" -> Carnivore, "eat plants" -> Herbivore
        if re.search(r'\b(?:eat|eats|eating)\s+(?:meat|flesh|animals)\b', q):
            filters["diet"] = "Carnivore"
            params["diet_name"] = "Carnivore"
        elif re.search(r'\b(?:eat|eats|eating)\s+(?:plants|vegetation)\b', q):
            filters["diet"] = "Herbivore"
            params["diet_name"] = "Herbivore"

        # ---------------------------------------------------------
        # 4. Detect Taxonomic Class
        # ---------------------------------------------------------
        for term, canonical in CLASS_KEYWORDS.items():
            if re.search(r'\b' + re.escape(term) + r'\b', q):
                # Disambiguation: If preceded by 'eat/eats/eating' (e.g. 'eats fish'),
                # this is a food item, NOT a class constraint!
                if not re.search(r'\b(?:eat|eats|eating)\s+(?:a\s+|an\s+|the\s+)?' + re.escape(term) + r'\b', q):
                    filters["class"] = canonical
                    params["class_name"] = canonical
                    break

        # ---------------------------------------------------------
        # 5. Detect Continent
        # ---------------------------------------------------------
        for term, canonical in CONTINENT_KEYWORDS.items():
            if re.search(r'\b' + re.escape(term) + r'\b', q):
                filters["continent"] = canonical
                params["continent_name"] = canonical
                break

        # ---------------------------------------------------------
        # 6. Detect Food / Prey Source
        # ---------------------------------------------------------
        for term, canonical in FOOD_KEYWORDS.items():
            if re.search(r'\b' + re.escape(term) + r'\b', q):
                filters["food"] = canonical
                params["food_name"] = canonical
                break

        # ---------------------------------------------------------
        # 7. Synthesize Parameterized Cypher Query
        # ---------------------------------------------------------
        match_clauses = ["(a:Animal)"]
        where_conditions = []

        if "status" in filters:
            match_clauses.append("(a)-[:HAS_STATUS]->(cs:ConservationStatus)")
            where_conditions.append("cs.name = $status_name")

        if is_water_query:
            match_clauses.append("(a)-[:LIVES_IN]->(h:Habitat)")
            where_conditions.append("h.name IN $water_habitats")
        elif is_land_query:
            match_clauses.append("(a)-[:LIVES_IN]->(h:Habitat)")
            where_conditions.append("h.name IN $land_habitats")
        elif "habitat" in filters:
            match_clauses.append("(a)-[:LIVES_IN]->(h:Habitat)")
            where_conditions.append("h.name = $habitat_name")
        elif "habitats" in filters:
            # Multi-habitat conjunction (e.g. lives in both forests and grasslands)
            for idx, hab in enumerate(filters["habitats"]):
                match_clauses.append(f"(a)-[:LIVES_IN]->(h{idx}:Habitat)")
                where_conditions.append(f"h{idx}.name = '{hab}'")

        if "diet" in filters:
            match_clauses.append("(a)-[:HAS_DIET]->(d:Diet)")
            where_conditions.append("d.name = $diet_name")

        if "class" in filters:
            match_clauses.append("(a)-[:BELONGS_TO_SPECIES]->(s:Species)-[:BELONGS_TO_CLASS]->(c:Class)")
            where_conditions.append("c.name = $class_name")

        if "continent" in filters:
            match_clauses.append("(a)-[:FOUND_IN]->(ct:Continent)")
            where_conditions.append("ct.name = $continent_name")

        if "food" in filters:
            match_clauses.append("(a)-[:EATS]->(f:Food)")
            where_conditions.append("toLower(f.name) = toLower($food_name)")

        matches_str = ",\n     ".join(match_clauses)
        where_str = ("\nWHERE " + " AND ".join(where_conditions)) if where_conditions else ""

        # Compose final Cypher query with optional contextual expansions
        cypher_query = f"""MATCH {matches_str}{where_str}
OPTIONAL MATCH (a)-[:BELONGS_TO_SPECIES]->(sp:Species)-[:BELONGS_TO_CLASS]->(cl:Class)
OPTIONAL MATCH (a)-[:HAS_STATUS]->(cstat:ConservationStatus)
OPTIONAL MATCH (a)-[:HAS_DIET]->(dt:Diet)
OPTIONAL MATCH (a)-[:LIVES_IN]->(hab:Habitat)
OPTIONAL MATCH (a)-[:FOUND_IN]->(con:Continent)
RETURN DISTINCT a.id AS id,
       a.name AS name,
       a.scientificName AS scientificName,
       a.description AS description,
       a.averageLifespan AS averageLifespan,
       a.imageUrl AS imageUrl,
       cl.name AS className,
       cstat.name AS conservationStatus,
       dt.name AS diet,
       collect(DISTINCT hab.name) AS habitats,
       collect(DISTINCT con.name) AS continents
ORDER BY a.name"""

        return filters, cypher_query, params

    @classmethod
    def execute_natural_language_query(cls, question: str) -> NaturalLanguageQueryResponse:
        """
        Executes a natural language query end-to-end:
        Extracts entities -> Compiles Cypher -> Runs against Neo4j -> Formats response.

        Args:
            question (str): Plain-English question from user.

        Returns:
            NaturalLanguageQueryResponse: Payload with extracted filters, generated Cypher,
                                          list of matched entities, and narrative explanation.
        """
        filters, cypher, params = cls.parse_natural_language_question(question)

        # Execute against live Neo4j database if connected
        if neo4j_client.is_connected:
            try:
                records = neo4j_client.execute_read(cypher, params)
                results = [AnimalSummary(**row) for row in records]
                explanation = cls._generate_explanation(filters, len(results))
                return NaturalLanguageQueryResponse(
                    question=question,
                    detectedFilters=filters,
                    cypherQuery=cypher,
                    results=results,
                    resultCount=len(results),
                    explanation=explanation
                )
            except Exception as e:
                logger.error("Error executing NL Cypher query on Neo4j: %s", str(e))

        # Fallback: In-memory simulation over ANIMALS_DATA
        water_habitats = {"Ocean", "River", "Wetland"}
        land_habitats = {"Forest", "Grassland", "Savanna", "Desert", "Mountain"}

        filtered = []
        for a in ANIMALS_DATA:
            match = True
            if "status" in filters and a["status"] != filters["status"]:
                match = False

            if "habitat" in filters:
                if filters["habitat"] == "Water (Ocean / River / Wetland)":
                    if not any(h in water_habitats for h in a["habitats"]):
                        match = False
                elif filters["habitat"] == "Land (Forest / Grassland / Savanna / Desert / Mountain)":
                    if not any(h in land_habitats for h in a["habitats"]):
                        match = False
                elif filters["habitat"] not in a["habitats"]:
                    match = False

            if "habitats" in filters and not all(h in a["habitats"] for h in filters["habitats"]):
                match = False
            if "diet" in filters and a["diet"] != filters["diet"]:
                match = False
            if "class" in filters and a["class"] != filters["class"]:
                match = False
            if "continent" in filters and filters["continent"] not in a["continents"]:
                match = False
            if "food" in filters and not any(f.lower() == filters["food"].lower() for f in a["foods"]):
                match = False

            if match:
                filtered.append(
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

        explanation = cls._generate_explanation(filters, len(filtered))
        return NaturalLanguageQueryResponse(
            question=question,
            detectedFilters=filters,
            cypherQuery=cypher,
            results=filtered,
            resultCount=len(filtered),
            explanation=explanation
        )

    @staticmethod
    def _generate_explanation(filters: Dict[str, Any], count: int) -> str:
        """Constructs an academic explanation string describing the active graph traversal constraints."""
        if not filters:
            return f"Retrieved {count} animals matching general criteria."
        parts = []
        for k, v in filters.items():
            if isinstance(v, list):
                parts.append(f"{k} = [{', '.join(v)}]")
            else:
                parts.append(f"{k} = '{v}'")
        return f"Identified graph constraints: {', '.join(parts)}. Found {count} matching animal entities."
