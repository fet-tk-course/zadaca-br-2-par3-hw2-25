[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Aplikacija pokriva domenu Svjetskog fudbalskog prvenstva 2026. API omogućava upravljanje podacima o utakmicama i državama sudionicama turnira. Implementirana je kao REST API koristeći FastAPI framework sa SQLite bazom podataka.

## Tim

- **Student A**: [Elvir Mustafić] - resurs: `/matches`
- **Student B**: [Faris Ćosić] - resurs: `/countries`

## Instalacija i pokretanje

### Preduvjeti

- Python 3.10 ili noviji
- pip

### Koraci

1. Klonirajte repozitorij:
```bash
git clone <url-repozitorija>
cd <naziv-repozitorija>
```

2. Kreirajte virtuelno okruženje:
```bash
python -m venv venv
```

3. Aktivirajte virtuelno okruženje:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalirajte zavisnosti:
```bash
pip install -r requirements.txt
```

5. Pokrenite aplikaciju:
```bash
uvicorn main:app --reload
```

6. Otvorite browser na adresi: `http://localhost:8000/docs`

## API Endpointi

### Resurs A: `/matches` (Utakmice)

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/matches` | Lista svih utakmica (filteri: `group`, `city`, `is_finished`, `stage`) |
| GET | `/matches/{id}` | Dohvatanje utakmice po ID-u |
| POST | `/matches` | Kreiranje nove utakmice (status 201) |
| PUT | `/matches/{id}` | Potpuna zamjena utakmice |
| PATCH | `/matches/{id}` | Djelimično ažuriranje utakmice |
| DELETE | `/matches/{id}` | Brisanje utakmice (status 204) |
| POST | `/matches/seed` | Punjenje baze sa 72 grupne utakmice SP 2026 |

**Primjeri zahtjeva:**
```bash
# Dohvatanje svih utakmica iz grupe L (Hrvatska, Engleska, Gana, Panama)
curl -X GET "http://localhost:8000/matches?group=L"

# Dohvatanje svih nezavršenih utakmica
curl -X GET "http://localhost:8000/matches?is_finished=false"

# Kreiranje nove utakmice
curl -X POST "http://localhost:8000/matches" \
  -H "Content-Type: application/json" \
  -d '{
    "group": "L",
    "home_team": "Croatia",
    "away_team": "England",
    "match_date": "2026-06-17",
    "match_time": "22:00",
    "city": "Dallas",
    "stage": "Group Stage"
  }'

# Ažuriranje rezultata utakmice
curl -X PATCH "http://localhost:8000/matches/70" \
  -H "Content-Type: application/json" \
  -d '{
    "home_score": 1,
    "away_score": 0,
    "is_finished": true
  }'
```

### Resurs B: `/countries`

[Kolega popunjava svoj dio]

## Korištenje AI alata

### Student A - Utakmice (`/matches`)
**Alat:** Claude (Anthropic)  
**Model:** Claude Sonnet 4.6

**Primjer 1:**
- **Prompt:** "Generiši SQLModel entitet za utakmicu na Svjetskom fudbalskom prvenstvu sa najmanje 5 polja različitih tipova, uključujući Optional polja, float i bool."
- **Kako je pomoglo:** AI je generisao osnovnu strukturu Match klase sa svim potrebnim poljima i tipovima podataka.
- **Prilagodbe:** Dodana su polja `match_time` i `city` specifična za SP 2026, te prilagođeni komentari na bosanskom jeziku.

**Primjer 2:**
- **Prompt:** "Napiši FastAPI CRUD rute za Match entitet koristeći Depends za session, sa 404 greškama i exclude_unset=True za PATCH endpoint, uključujući seed endpoint sa stvarnim podacima utakmica SP 2026."
- **Kako je pomoglo:** AI je generisao kompletan CRUD sa svim endpointima i seed podacima za svih 72 grupne utakmice.
- **Prilagodbe:** Prilagođene su poruke grešaka na bosanski jezik i dodan je filter po gradu (`city`) koji nije bio u originalnom prijedlogu.

### Student B - Države (`/countries`)

[Kolega popunjava svoj dio]

## Napomene

- Pokretanjem `POST /matches/seed` puni se baza sa svih 72 grupnih utakmica SP 2026 sa tačnim datumima, vremenima i gradovima.
- Svi komentari u kodu su na bosanskom jeziku, nazivi funkcija i varijabli na engleskom.
- Aplikacija je testirana putem Swagger dokumentacije na `http://localhost:8000/docs`.