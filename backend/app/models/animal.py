"""
Data Models for Animal Entities and Dashboard Metrics.

Defines Pydantic schemas for serialized responses:
- AnimalSummary: Compact payload for cards, lists, and filter results.
- AnimalDetail: Comprehensive profile including taxonomy, biomes, diet, and food chain.
- DashboardStats: Aggregate graph counts displayed on the home overview dashboard.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AnimalSummary(BaseModel):
    """
    Compact representation of an Animal entity for listing and card views.
    """
    id: str = Field(..., description="Unique entity identifier (e.g. 'animal_tiger')")
    name: str = Field(..., description="Common vernacular name (e.g. 'Tiger')")
    scientificName: Optional[str] = Field(None, description="Latin binomial name (e.g. 'Panthera tigris')")
    description: Optional[str] = Field(None, description="Short ecological summary")
    averageLifespan: Optional[int] = Field(None, description="Average lifespan in years")
    imageUrl: Optional[str] = Field(None, description="CDN URL pointing to a high-resolution photograph")
    className: Optional[str] = Field(None, description="Taxonomic class (Mammal, Bird, Reptile, etc.)")
    conservationStatus: Optional[str] = Field(None, description="IUCN status (Endangered, Vulnerable, etc.)")
    diet: Optional[str] = Field(None, description="Dietary classification (Carnivore, Herbivore, etc.)")
    habitats: List[str] = Field(default_factory=list, description="List of habitats inhabited by this animal")
    continents: List[str] = Field(default_factory=list, description="Geographic continents where this animal is found")


class AnimalDetail(BaseModel):
    """
    Detailed graph profile for an Animal entity, returned by /api/animals/{id}.
    Includes direct taxonomic links, biomes, prey/food sources, and distribution.
    """
    id: str = Field(..., description="Unique entity identifier")
    name: str = Field(..., description="Common vernacular name")
    scientificName: Optional[str] = Field(None, description="Latin binomial name")
    description: Optional[str] = Field(None, description="Comprehensive biological description")
    averageLifespan: Optional[int] = Field(None, description="Average lifespan in years")
    imageUrl: Optional[str] = Field(None, description="CDN photograph URL")
    species: Optional[str] = Field(None, description="Common name of parent species")
    speciesScientificName: Optional[str] = Field(None, description="Scientific name of parent species")
    className: Optional[str] = Field(None, description="Taxonomic class")
    diet: Optional[str] = Field(None, description="Diet classification")
    conservationStatus: Optional[str] = Field(None, description="Conservation status")
    habitats: List[str] = Field(default_factory=list, description="All associated habitat biomes")
    foodSources: List[str] = Field(default_factory=list, description="Food sources and prey eaten by this animal")
    continents: List[str] = Field(default_factory=list, description="All native geographical continents")


class DashboardStats(BaseModel):
    """
    High-level aggregate metrics for the knowledge graph.
    """
    totalAnimals: int = Field(..., description="Total count of (:Animal) nodes")
    totalSpecies: int = Field(..., description="Total count of (:Species) nodes")
    totalHabitats: int = Field(..., description="Total count of (:Habitat) nodes")
    totalFoods: int = Field(..., description="Total count of (:Food) nodes")
    totalEndangeredAnimals: int = Field(..., description="Count of animals with Endangered / Critically Endangered status")
    totalContinents: int = Field(..., description="Total count of (:Continent) nodes")
    neo4jConnected: bool = Field(True, description="Flag indicating live connection to Neo4j instance")
