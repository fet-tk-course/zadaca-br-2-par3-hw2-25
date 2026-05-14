from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator



# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 

class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
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

@field_validator('grupa')
@classmethod
def grupaProvjera(cls, v):
    if v not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        raise ValueError('Netačna grupa')
    return v
    
@field_validator('ime')
@classmethod
def imeNePrazno(cls, v):
    if not v.strip():
        raise ValueError("Ime ne smije biti prazno!")
    return v.strip()
    
@field_validator('ranking')
@classmethod
def rankingVeciOdJedan(cls, v):
    if v < 1:
        raise ValueError("Ranking mora biti veci od 1")
    return v
@field_validator('pobjede')
@classmethod
def pobjedePozitivne(cls, v):
    if v < 0:
        raise ValueError('Broj pobjeda mora biti veci od 0')
    return v
    
@field_validator('kontinent')
@classmethod
def kontinentPrazan(cls, v):
    if not v.strip():
        raise ValueError('Kontinent ne moze biti prazan')
    return v

class CountryUpdate(SQLModel):
    name: Optional[str] = None
    group: Optional[str] = None  
    fifa_ranking: Optional[int] = None
    continent: Optional[str] = None
    world_cup_wins: Optional[int] = None
