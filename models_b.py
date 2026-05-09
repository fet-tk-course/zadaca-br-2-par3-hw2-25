from sqlmodel import SQLModel, Field
from typing import Optional

# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 

class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    group: str  
    fifa_ranking: int
    continent: str
    world_cup_wins: int
    
class CountryCreate(SQLModel):
    name: str
    group: str  
    fifa_ranking: int
    continent: str
    world_cup_wins: int

class CountryUpate(SQLModel):
    name: Optional[str] = None
    group: Optional[str] = None  
    fifa_ranking: Optional[int] = None
    continent: Optional[str] = None
    world_cup_wins: Optional[int] = None