from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session

from models_b import Country, CountryCreate, CountryUpate

router = APIRouter(prefix="/country", tags=["Country"])

@router.get("/")
def get_countries(session: Session = Depends(get_session)):
    countries = session.exec(select(Country)).all()
    return countries
