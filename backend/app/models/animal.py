from typing import List, Optional
from pydantic import BaseModel, Field

class AnimalSummary(BaseModel):
    id: str
    name: str
    scientificName: Optional[str] = None
    description: Optional[str] = None
    averageLifespan: Optional[int] = None
    imageUrl: Optional[str] = None
    className: Optional[str] = None
    conservationStatus: Optional[str] = None
    diet: Optional[str] = None
    habitats: List[str] = Field(default_factory=list)
    continents: List[str] = Field(default_factory=list)

class AnimalDetail(BaseModel):
    id: str
    name: str
    scientificName: Optional[str] = None
    description: Optional[str] = None
    averageLifespan: Optional[int] = None
    imageUrl: Optional[str] = None
    species: Optional[str] = None
    speciesScientificName: Optional[str] = None
    className: Optional[str] = None
    diet: Optional[str] = None
    conservationStatus: Optional[str] = None
    habitats: List[str] = Field(default_factory=list)
    foodSources: List[str] = Field(default_factory=list)
    continents: List[str] = Field(default_factory=list)

class DashboardStats(BaseModel):
    totalAnimals: int
    totalSpecies: int
    totalHabitats: int
    totalFoods: int
    totalEndangeredAnimals: int
    totalContinents: int
    neo4jConnected: bool = True
