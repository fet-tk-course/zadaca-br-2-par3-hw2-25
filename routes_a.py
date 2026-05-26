from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from database import get_session
from models_a import Match, MatchCreate, MatchUpdate

# Kreiranje APIRouter instance za utakmice
router = APIRouter(prefix="/matches", tags=["Matches"])


"""Pomocna funkcija koja vraća listu svih grupnih utakmica SP 2026 kao seed podatke."""
def get_seed_matches() -> List[dict]:
    """Vraća listu svih grupnih utakmica SP 2026 kao seed podatke."""
    return [
        # --- SKUPINA A ---
        {"group": "A", "home_team": "Mexico",       "away_team": "South Africa", "match_date": "2026-06-11", "match_time": "21:00", "city": "Mexico City",   "stage": "Group Stage"},
        {"group": "A", "home_team": "South Korea",  "away_team": "Czech Republic","match_date": "2026-06-12", "match_time": "04:00", "city": "Guadalajara",   "stage": "Group Stage"},
        {"group": "A", "home_team": "Czech Republic","away_team": "South Africa", "match_date": "2026-06-18", "match_time": "18:00", "city": "Atlanta",       "stage": "Group Stage"},
        {"group": "A", "home_team": "Mexico",       "away_team": "South Korea",  "match_date": "2026-06-19", "match_time": "03:00", "city": "Guadalajara",   "stage": "Group Stage"},
        {"group": "A", "home_team": "Czech Republic","away_team": "Mexico",       "match_date": "2026-06-25", "match_time": "03:00", "city": "Mexico City",   "stage": "Group Stage"},
        {"group": "A", "home_team": "South Africa", "away_team": "South Korea",  "match_date": "2026-06-25", "match_time": "03:00", "city": "Monterrey",     "stage": "Group Stage"},
        # --- SKUPINA B ---
        {"group": "B", "home_team": "Canada",       "away_team": "Bosnia and Herzegovina", "match_date": "2026-06-12", "match_time": "21:00", "city": "Toronto",       "stage": "Group Stage"},
        {"group": "B", "home_team": "Qatar",        "away_team": "Switzerland",  "match_date": "2026-06-13", "match_time": "21:00", "city": "San Francisco", "stage": "Group Stage"},
        {"group": "B", "home_team": "Switzerland",  "away_team": "Bosnia and Herzegovina", "match_date": "2026-06-18", "match_time": "21:00", "city": "Los Angeles",   "stage": "Group Stage"},
        {"group": "B", "home_team": "Canada",       "away_team": "Qatar",        "match_date": "2026-06-19", "match_time": "00:00", "city": "Vancouver",     "stage": "Group Stage"},
        {"group": "B", "home_team": "Switzerland",  "away_team": "Canada",       "match_date": "2026-06-24", "match_time": "21:00", "city": "Vancouver",     "stage": "Group Stage"},
        {"group": "B", "home_team": "Bosnia and Herzegovina", "away_team": "Qatar", "match_date": "2026-06-24", "match_time": "21:00", "city": "Seattle",    "stage": "Group Stage"},
        # --- SKUPINA C ---
        {"group": "C", "home_team": "Brazil",       "away_team": "Morocco",      "match_date": "2026-06-14", "match_time": "00:00", "city": "New Jersey",    "stage": "Group Stage"},
        {"group": "C", "home_team": "Haiti",        "away_team": "Scotland",     "match_date": "2026-06-14", "match_time": "03:00", "city": "Boston",        "stage": "Group Stage"},
        {"group": "C", "home_team": "Scotland",     "away_team": "Morocco",      "match_date": "2026-06-20", "match_time": "00:00", "city": "Boston",        "stage": "Group Stage"},
        {"group": "C", "home_team": "Brazil",       "away_team": "Haiti",        "match_date": "2026-06-20", "match_time": "02:30", "city": "Philadelphia",  "stage": "Group Stage"},
        {"group": "C", "home_team": "Scotland",     "away_team": "Brazil",       "match_date": "2026-06-25", "match_time": "00:00", "city": "Miami",         "stage": "Group Stage"},
        {"group": "C", "home_team": "Morocco",      "away_team": "Haiti",        "match_date": "2026-06-25", "match_time": "00:00", "city": "Atlanta",       "stage": "Group Stage"},
        # --- SKUPINA D ---
        {"group": "D", "home_team": "USA",          "away_team": "Paraguay",     "match_date": "2026-06-13", "match_time": "03:00", "city": "Los Angeles",   "stage": "Group Stage"},
        {"group": "D", "home_team": "Australia",    "away_team": "Turkey",       "match_date": "2026-06-14", "match_time": "06:00", "city": "Vancouver",     "stage": "Group Stage"},
        {"group": "D", "home_team": "USA",          "away_team": "Australia",    "match_date": "2026-06-19", "match_time": "21:00", "city": "Seattle",       "stage": "Group Stage"},
        {"group": "D", "home_team": "Turkey",       "away_team": "Paraguay",     "match_date": "2026-06-20", "match_time": "05:00", "city": "San Francisco", "stage": "Group Stage"},
        {"group": "D", "home_team": "Turkey",       "away_team": "USA",          "match_date": "2026-06-26", "match_time": "04:00", "city": "Los Angeles",   "stage": "Group Stage"},
        {"group": "D", "home_team": "Paraguay",     "away_team": "Australia",    "match_date": "2026-06-26", "match_time": "04:00", "city": "San Francisco", "stage": "Group Stage"},
        # --- SKUPINA E ---
        {"group": "E", "home_team": "Germany",      "away_team": "Curacao",      "match_date": "2026-06-14", "match_time": "19:00", "city": "Houston",       "stage": "Group Stage"},
        {"group": "E", "home_team": "Ivory Coast",  "away_team": "Ecuador",      "match_date": "2026-06-15", "match_time": "01:00", "city": "Philadelphia",  "stage": "Group Stage"},
        {"group": "E", "home_team": "Germany",      "away_team": "Ivory Coast",  "match_date": "2026-06-20", "match_time": "22:00", "city": "Toronto",       "stage": "Group Stage"},
        {"group": "E", "home_team": "Ecuador",      "away_team": "Curacao",      "match_date": "2026-06-21", "match_time": "02:00", "city": "Kansas City",   "stage": "Group Stage"},
        {"group": "E", "home_team": "Ecuador",      "away_team": "Germany",      "match_date": "2026-06-25", "match_time": "22:00", "city": "New Jersey",    "stage": "Group Stage"},
        {"group": "E", "home_team": "Curacao",      "away_team": "Ivory Coast",  "match_date": "2026-06-25", "match_time": "22:00", "city": "Philadelphia",  "stage": "Group Stage"},
        # --- SKUPINA F ---
        {"group": "F", "home_team": "Netherlands",  "away_team": "Japan",        "match_date": "2026-06-14", "match_time": "22:00", "city": "Dallas",        "stage": "Group Stage"},
        {"group": "F", "home_team": "Sweden",       "away_team": "Tunisia",      "match_date": "2026-06-15", "match_time": "04:00", "city": "Monterrey",     "stage": "Group Stage"},
        {"group": "F", "home_team": "Netherlands",  "away_team": "Sweden",       "match_date": "2026-06-20", "match_time": "19:00", "city": "Houston",       "stage": "Group Stage"},
        {"group": "F", "home_team": "Tunisia",      "away_team": "Japan",        "match_date": "2026-06-21", "match_time": "06:00", "city": "Monterrey",     "stage": "Group Stage"},
        {"group": "F", "home_team": "Tunisia",      "away_team": "Netherlands",  "match_date": "2026-06-26", "match_time": "01:00", "city": "Kansas City",   "stage": "Group Stage"},
        {"group": "F", "home_team": "Japan",        "away_team": "Sweden",       "match_date": "2026-06-26", "match_time": "01:00", "city": "Dallas",        "stage": "Group Stage"},
        # --- SKUPINA G ---
        {"group": "G", "home_team": "Belgium",      "away_team": "Egypt",        "match_date": "2026-06-15", "match_time": "21:00", "city": "Seattle",       "stage": "Group Stage"},
        {"group": "G", "home_team": "Iran",         "away_team": "New Zealand",  "match_date": "2026-06-16", "match_time": "03:00", "city": "Los Angeles",   "stage": "Group Stage"},
        {"group": "G", "home_team": "Belgium",      "away_team": "Iran",         "match_date": "2026-06-21", "match_time": "21:00", "city": "Los Angeles",   "stage": "Group Stage"},
        {"group": "G", "home_team": "New Zealand",  "away_team": "Egypt",        "match_date": "2026-06-22", "match_time": "03:00", "city": "Vancouver",     "stage": "Group Stage"},
        {"group": "G", "home_team": "New Zealand",  "away_team": "Belgium",      "match_date": "2026-06-27", "match_time": "05:00", "city": "Vancouver",     "stage": "Group Stage"},
        {"group": "G", "home_team": "Egypt",        "away_team": "Iran",         "match_date": "2026-06-27", "match_time": "05:00", "city": "Seattle",       "stage": "Group Stage"},
        # --- SKUPINA H ---
        {"group": "H", "home_team": "Spain",        "away_team": "Cape Verde",   "match_date": "2026-06-15", "match_time": "18:00", "city": "Atlanta",       "stage": "Group Stage"},
        {"group": "H", "home_team": "Saudi Arabia", "away_team": "Uruguay",      "match_date": "2026-06-16", "match_time": "00:00", "city": "Miami",         "stage": "Group Stage"},
        {"group": "H", "home_team": "Spain",        "away_team": "Saudi Arabia", "match_date": "2026-06-21", "match_time": "18:00", "city": "Atlanta",       "stage": "Group Stage"},
        {"group": "H", "home_team": "Uruguay",      "away_team": "Cape Verde",   "match_date": "2026-06-22", "match_time": "00:00", "city": "Miami",         "stage": "Group Stage"},
        {"group": "H", "home_team": "Uruguay",      "away_team": "Spain",        "match_date": "2026-06-27", "match_time": "02:00", "city": "Guadalajara",   "stage": "Group Stage"},
        {"group": "H", "home_team": "Cape Verde",   "away_team": "Saudi Arabia", "match_date": "2026-06-27", "match_time": "02:00", "city": "Houston",       "stage": "Group Stage"},
        # --- SKUPINA I ---
        {"group": "I", "home_team": "France",       "away_team": "Senegal",      "match_date": "2026-06-16", "match_time": "21:00", "city": "New Jersey",    "stage": "Group Stage"},
        {"group": "I", "home_team": "Iraq",         "away_team": "Norway",       "match_date": "2026-06-17", "match_time": "00:00", "city": "Boston",        "stage": "Group Stage"},
        {"group": "I", "home_team": "France",       "away_team": "Iraq",         "match_date": "2026-06-22", "match_time": "23:00", "city": "Philadelphia",  "stage": "Group Stage"},
        {"group": "I", "home_team": "Norway",       "away_team": "Senegal",      "match_date": "2026-06-23", "match_time": "02:00", "city": "New Jersey",    "stage": "Group Stage"},
        {"group": "I", "home_team": "Norway",       "away_team": "France",       "match_date": "2026-06-26", "match_time": "21:00", "city": "Boston",        "stage": "Group Stage"},
        {"group": "I", "home_team": "Senegal",      "away_team": "Iraq",         "match_date": "2026-06-26", "match_time": "21:00", "city": "Toronto",       "stage": "Group Stage"},
        # --- SKUPINA J ---
        {"group": "J", "home_team": "Argentina",    "away_team": "Algeria",      "match_date": "2026-06-17", "match_time": "03:00", "city": "Kansas City",   "stage": "Group Stage"},
        {"group": "J", "home_team": "Austria",      "away_team": "Jordan",       "match_date": "2026-06-17", "match_time": "06:00", "city": "San Francisco", "stage": "Group Stage"},
        {"group": "J", "home_team": "Argentina",    "away_team": "Austria",      "match_date": "2026-06-22", "match_time": "19:00", "city": "Dallas",        "stage": "Group Stage"},
        {"group": "J", "home_team": "Jordan",       "away_team": "Algeria",      "match_date": "2026-06-23", "match_time": "05:00", "city": "San Francisco", "stage": "Group Stage"},
        {"group": "J", "home_team": "Jordan",       "away_team": "Argentina",    "match_date": "2026-06-28", "match_time": "04:00", "city": "Dallas",        "stage": "Group Stage"},
        {"group": "J", "home_team": "Algeria",      "away_team": "Austria",      "match_date": "2026-06-28", "match_time": "04:00", "city": "Kansas City",   "stage": "Group Stage"},
        # --- SKUPINA K ---
        {"group": "K", "home_team": "Portugal",     "away_team": "DR Congo",     "match_date": "2026-06-17", "match_time": "19:00", "city": "Houston",       "stage": "Group Stage"},
        {"group": "K", "home_team": "Uzbekistan",   "away_team": "Colombia",     "match_date": "2026-06-18", "match_time": "04:00", "city": "Mexico City",   "stage": "Group Stage"},
        {"group": "K", "home_team": "Portugal",     "away_team": "Uzbekistan",   "match_date": "2026-06-23", "match_time": "19:00", "city": "Houston",       "stage": "Group Stage"},
        {"group": "K", "home_team": "Colombia",     "away_team": "DR Congo",     "match_date": "2026-06-24", "match_time": "04:00", "city": "Guadalajara",   "stage": "Group Stage"},
        {"group": "K", "home_team": "Colombia",     "away_team": "Portugal",     "match_date": "2026-06-28", "match_time": "01:30", "city": "Miami",         "stage": "Group Stage"},
        {"group": "K", "home_team": "DR Congo",     "away_team": "Uzbekistan",   "match_date": "2026-06-28", "match_time": "01:30", "city": "Atlanta",       "stage": "Group Stage"},
        # --- SKUPINA L ---
        {"group": "L", "home_team": "Croatia",      "away_team": "England",      "match_date": "2026-06-17", "match_time": "22:00", "city": "Dallas",        "stage": "Group Stage"},
        {"group": "L", "home_team": "Ghana",        "away_team": "Panama",       "match_date": "2026-06-18", "match_time": "01:00", "city": "Toronto",       "stage": "Group Stage"},
        {"group": "L", "home_team": "England",      "away_team": "Ghana",        "match_date": "2026-06-23", "match_time": "22:00", "city": "Boston",        "stage": "Group Stage"},
        {"group": "L", "home_team": "Croatia",      "away_team": "Panama",       "match_date": "2026-06-24", "match_time": "01:00", "city": "Toronto",       "stage": "Group Stage"},
        {"group": "L", "home_team": "Panama",       "away_team": "England",      "match_date": "2026-06-27", "match_time": "23:00", "city": "New Jersey",    "stage": "Group Stage"},
        {"group": "L", "home_team": "Croatia",      "away_team": "Ghana",        "match_date": "2026-06-27", "match_time": "23:00", "city": "Philadelphia",  "stage": "Group Stage"},
    ]


"""POST /matches/seed – Seediranje/punjenje baze podataka grupnim utakmicama SP 2026"""
@router.post("/seed", tags=["Seed"], status_code=status.HTTP_201_CREATED)
def seed_matches(session: Session = Depends(get_session)):
    """Puni bazu podataka svim grupnim utakmicama SP 2026. Preskače utakmice koje već postoje."""
    existing = session.exec(select(Match)).all()
    existing_keys = {(m.home_team, m.away_team, m.match_date) for m in existing}

    added = 0
    for data in get_seed_matches():
        key = (data["home_team"], data["away_team"], data["match_date"])
        if key not in existing_keys:
            match = Match(**data)
            session.add(match)
            added += 1

    session.commit()
    return {"message": f"Seed završen. Dodano {added} utakmica."}


"""GET /matches – Dohvatanje svih utakmica"""
@router.get("/", response_model=List[Match])
def get_matches(
    group: Optional[str] = Query(default=None, description="Filtriraj po grupi (npr. A, B, C)"),
    city: Optional[str] = Query(default=None, description="Filtriraj po gradu (npr. Dallas, Miami)"),
    is_finished: Optional[bool] = Query(default=None, description="Filtriraj po statusu završenosti"),
    stage: Optional[str] = Query(default=None, description="Filtriraj po fazi (npr. Group Stage, Final)"),
    session: Session = Depends(get_session)
):
    """Vraća listu svih utakmica. Podržava filtriranje po grupi, gradu, statusu i fazi."""
    query = select(Match)

    # Primjena filtera ukoliko su zadani
    if group is not None:
        query = query.where(Match.group == group)
    if city is not None:
        query = query.where(Match.city == city)
    if is_finished is not None:
        query = query.where(Match.is_finished == is_finished)
    if stage is not None:
        query = query.where(Match.stage == stage)

    matches = session.exec(query).all()
    return matches

"""Ovo je kod za odbranu zadace dva radi lakseg snalazenja pri pregledu zadatak dva"""

@router.post("Izvlacenje_podataka_iz_baze", tags=["Seed"], status_code=status.HTTP_201_CREATED)
def pretraga_grupa(group: Optional[str] = Query(default=None, description="Filtriranje_po_grupi"), session: Session = Depends(get_session)):
  
    if group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Polje grupa je obavezan.")
    utakmice = session.exec(select(Match).where(Match.group == group)).all()
    if not utakmice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nema_utakmica_u_ovoj_grupi {group}.")
    return utakmice



"""GET /matches/{id} – Dohvatanje jedne utakmice po ID-u"""
@router.get("/{match_id}", response_model=Match)
def get_match(match_id: int, session: Session = Depends(get_session)):
    """Vraća jednu utakmicu po ID-u. Vraća 404 ako ne postoji."""
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utakmica sa ID-om {match_id} nije pronađena."
        )
    return match


"""POST /matches/ – Kreiranje nove utakmice"""
@router.post("/", response_model=Match, status_code=status.HTTP_201_CREATED)
def create_match(match_data: MatchCreate, session: Session = Depends(get_session)):
    """Kreira novu utakmicu i sprema je u bazu. Vraća 201 status."""


    """Ovo je kod za odbranu zadace dva radi lakseg snalazenja pri pregledu zadatak 1b"""

    existing = session.exec(select(math).where(match.home_team == match_data.home_team. and match.away_team == match_data.away_team, and match.match_date == match_data.match_date)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP 422 Unprocessable Entity, detail="Na ovaj datum vec postoji ova utakmica.")
    
    
    
    match = Match.model_validate(match_data)
    session.add(match)
    session.commit()
    session.refresh(match)
    return match



"""PUT /matches/{id} – Potpuno ažuriranje utakmice"""
@router.put("/{match_id}", response_model=Match)
def update_match(match_id: int, match_data: MatchCreate, session: Session = Depends(get_session)):
    """Potpuno zamjenjuje podatke utakmice. Vraća 404 ako ne postoji."""
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utakmica sa ID-om {match_id} nije pronađena."
        )

    # Zamjena svih polja novim vrijednostima
    match_dict = match_data.model_dump()
    for key, value in match_dict.items():
        setattr(match, key, value)

    session.add(match)
    session.commit()
    session.refresh(match)
    return match


"""PATCH /matches/{id} – Djelimično ažuriranje utakmice"""
@router.patch("/{match_id}", response_model=Match)
def partial_update_match(match_id: int, match_data: MatchUpdate, session: Session = Depends(get_session)):
    """Djelimično ažurira utakmicu – mijenja samo poslana polja. Vraća 404 ako ne postoji."""
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utakmica sa ID-om {match_id} nije pronađena."
        )

    # exclude_unset=True osigurava da se ažuriraju samo eksplicitno poslana polja
    update_data = match_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(match, key, value)

    session.add(match)
    session.commit()
    session.refresh(match)
    return match


"""DELETE /matches/{id} – Brisanje utakmice"""
@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, session: Session = Depends(get_session)):
    """Briše utakmicu iz baze. Vraća 204 ako je uspješno, 404 ako ne postoji."""
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utakmica sa ID-om {match_id} nije pronađena."
        )

    session.delete(match)
    session.commit()
    # 204 No Content – ne vraća tijelo odgovora