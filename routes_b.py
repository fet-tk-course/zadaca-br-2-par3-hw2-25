from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional

from database import get_session

from models_b import Country, CountryCreate, CountryUpdate

router = APIRouter(prefix="/countries", tags=["Country"])

@router.get("/")
def get_countries(name : Optional[str] = None, group : Optional[str] = None, continent : Optional[str] = None, session: Session = Depends(get_session)):
    query = select(Country)
    if name:
        query = query.where(Country.name == name)
    if group:
        query = query.where(Country.group == group)
    if continent:
        query = query.where(Country.continent == continent)
    countries = session.exec(query).all()
    return countries

@router.get("/{country_id}")
def get_country(country_id: int, session: Session = Depends(get_session)):
    country = session.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Država nije pronađena")
    return country

@router.post("/")
def create_country(country: CountryCreate, session: Session = Depends(get_session)):
    new_country = Country.from_orm(country)
    session.add(new_country)
    session.commit()
    session.refresh(new_country)
    return new_country

@router.put("/{country_id}")
def update_country(country_id: int, country_update: CountryCreate, session: Session = Depends(get_session)):
    country = session.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Država nije pronađena")
    
    country_data = country_update.dict()
    for key, value in country_data.items():
        setattr(country, key, value)
    
    session.add(country)
    session.commit()
    session.refresh(country)
    return country

@router.patch("/{country_id}")
def patch_country(country_id: int, country_update: CountryUpdate, session: Session = Depends(get_session)):
    country = session.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Država nije pronađena")
    
    country_data = country_update.dict(exclude_unset=True)
    for key, value in country_data.items():
        setattr(country, key, value)
    
    session.add(country)
    session.commit()
    session.refresh(country)
    return country

@router.delete("/{country_id}", status_code=204)
def delete_country(country_id: int, session: Session = Depends(get_session)):
    country = session.get(Country, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Država nije pronađena")
    
    session.delete(country)
    session.commit()
    return