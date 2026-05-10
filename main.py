from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import create_db_and_tables
from routes_a import router as matches_router

# NAPOMENA ZA KOLEGU: Dodati import ispod i registrirati router
# from routes_b import router as countries_router


"""Kreira tabelu i baze podataka prilikom pokretanja aplikacije"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup event: kreira bazu i tabele ako ne postoje."""
    create_db_and_tables()
    yield

"""Kreiranje FastAPI instance"""
app = FastAPI(
    title="World Cup 2026 API",
    description="REST API za upravljanje podacima Svjetskog fudbalskog prvenstva 2026.",
    version="1.0.0",
    lifespan=lifespan
)

 
app.include_router(matches_router)

# NAPOMENA ZA KOLEGU: Uncommentati nakon merge-a
# app.include_router(countries_router)


"""Endpoint RUTE"""
@app.get("/")
def root():
    """Dobrodošlica – provjera da li je API aktivan."""
    return {
        "message": "World Cup 2026 API je aktivan.",
        "docs": "/docs",
        "endpoints": ["/matches", "/countries"]
    }