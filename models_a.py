from typing import Optional
from sqlmodel import SQLModel, Field


"""Glavni entiteti za utakmicu na Svjetskom fudbalskom prvenstvu 2026."""
class Match(SQLModel, table=True):
    """SQLModel entitet koji predstavlja utakmicu na Svjetskom fudbalskom prvenstvu 2026."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # Naziv grupe (npr. "A", "B", ..., "L")
    group: str = Field(max_length=1)

    # Domaća reprezentacija
    home_team: str

    # Gostujuća reprezentacija
    away_team: str

    # Datum utakmice u formatu YYYY-MM-DD (npr. "2026-06-11")
    match_date: str

    # Lokalno vrijeme utakmice (npr. "21:00")
    match_time: str

    # Grad održavanja utakmice (npr. "Mexico City")
    city: str

    # Golovi domaće reprezentacije (None ako utakmica nije odigrana)
    home_score: Optional[int] = None

    # Golovi gostujuće reprezentacije (None ako utakmica nije odigrana)
    away_score: Optional[int] = None

    # Da li je utakmica završena
    is_finished: bool = Field(default=False)

    # Faza takmičenja (Group Stage, Round of 32, Quarter-final, Semi-final, Final)
    stage: str = Field(default="Group Stage")


"""Šema za kreiranje nove utakmice"""
class MatchCreate(SQLModel):
    """Shema koja se koristi pri POST zahtjevu za kreiranje nove utakmice."""
    group: str
    home_team: str
    away_team: str
    match_date: str
    match_time: str
    city: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    is_finished: bool = False
    stage: str = "Group Stage"

"""Šema za djelimičnu izmjenu utakmice"""
class MatchUpdate(SQLModel):
    """Shema koja se koristi pri PATCH zahtjevu – sva polja su opcionalna."""
    group: Optional[str] = None
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    match_date: Optional[str] = None
    match_time: Optional[str] = None
    city: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    is_finished: Optional[bool] = None
    stage: Optional[str] = None