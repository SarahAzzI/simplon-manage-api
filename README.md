# Simplon Manage API 🚀

API REST pour la gestion d'un centre de formation Simplon. Permet de gérer les utilisateurs, les formations, les sessions et les inscriptions.

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Base de données**: SQLite
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Tests**: Pytest (94% couverture)

## 🚀 Installation & Lancement

### 1. Cloner le projet
```bash
git clone <url-repo>
cd simplon-manage-api
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou .\venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données (Migrations)
```bash
alembic upgrade head
```

### 5. Lancer l'application
```bash
uvicorn app.main:app --reload
```
L'API sera disponible sur `http://127.0.0.1:8000`.
La documentation Swagger est accessible sur `http://127.0.0.1:8000/docs`.

## 🧪 Tests

Pour lancer la suite de tests complète (41 tests) et voir le rapport de couverture :
```bash
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

## 🏗 Architecture

- `app/models/`: Modèles SQLAlchemy (Database tables)
- `app/schemas/`: Schémas Pydantic (Data validation / DTOs)
- `app/services/`: Logique métier (Business logic)
- `app/routes/`: Points d'entrée API (Endpoints)
- `app/core/`: Configuration et exceptions centralisées
- `alembic/`: Gestion des migrations de base de données

## 📝 Fonctionnalités clés

- **Utilisateurs**: Gestion des rôles (Administrateur, Formateur, Étudiant), Soft delete.
- **Formations**: Catalogue des formations avec niveaux et durées.
- **Sessions**: Planification des sessions avec validation de dates et capacité.
- **Inscriptions**: Inscription des étudiants avec contrôle de doublons et de capacité maximale.
- **Pagination**: Standardisée sur tous les endpoints de liste (`page`, `size`).
- **Filtrage**: Recherche de sessions par formation ou formateur.
