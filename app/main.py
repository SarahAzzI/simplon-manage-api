
from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes import user, formation, session, inscription

app = FastAPI(
    title="API Centre de Formation — Simplon",
    description="API REST pour la gestion des formations, sessions et inscriptions",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine) 

# ENREGISTREMENT DES ROUTES (routers)
# Chaque ligne connecte un fichier routes/*.py à l'API
# Sans ces lignes → les endpoints n'existent PAS

app.include_router(user.router)   # → /utilisateurs/
app.include_router(formation.router)     # → /formations/
app.include_router(session.router)       # → /sessions/
app.include_router(inscription.router)   # → /inscriptions/


# HEALTH CHECK
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "API Centre de Formation opérationnelle",
    }