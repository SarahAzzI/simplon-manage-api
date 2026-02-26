# Plan de Mise en Œuvre — API Simplon

Ce document définit les étapes de développement de l'API de gestion pour le centre de formation Simplon.

## Stack Technique
- **Framework :** FastAPI
- **Base de données :** SQLite3
- **ORM :** SQLAlchemy
- **Migrations :** Alembic
- **Validation :** Pydantic v2
- **Tests :** Pytest

---

## Étapes du Projet

### 1. Setup & Architecture (Jours 1–2)
- [ ] **Modélisation des données :** Finaliser les modèles SQLAlchemy dans `app/models/`.
  - `User` : Roles (Admin, Formateur, Apprenant).
  - `Formation` : Titre, description, durée, niveau.
  - `SessionFormation` : Dates, capacité, relations.
  - `Inscription` : Table de liaison avec contraintes d'unicité.
- [ ] **DTOs (Schémas) :** Créer les schémas Pydantic dans `app/schemas/` pour chaque entité (Base, Create, Update, Read).
- [ ] **Migrations initiales :** Configurer Alembic et générer la première migration pour créer les tables SQLite.

### 2. Développement des Services & CRUD (Jours 3–5)
- [ ] **Services :** Implémenter la logique métier dans `app/services/`.
  - CRUD complet pour les Utilisateurs.
  - CRUD complet pour les Formations.
  - CRUD complet pour les Sessions.
- [ ] **Logique d'inscription :** Implémenter le service d'inscription avec vérification de la capacité maximale de la session.
- [ ] **Routes :** Connecter les services aux endpoints FastAPI dans `app/routes/`.

### 3. Fonctionnalités Avancées (Jours 6–7)
- [ ] **Gestion des erreurs :** Centraliser les exceptions (404, 400, etc.) pour des réponses API cohérentes.
- [ ] **Pagination & Filtres :** Ajouter la pagination sur les listes et des filtres (ex: filtrer les sessions par formateur).
- [ ] **Tests automatisés :** Créer la suite de tests avec Pytest.
  - Tests unitaires des services (règles métier).
  - Tests d'intégration des endpoints (FastAPI TestClient).

### 4. Finalisation (Jour 8)
- [ ] **Documentation :** Compléter le `README.md` et s'assurer que Swagger est bien documenté.
- [ ] **Peuplement (Seed) :** (Optionnel) Créer un script pour injecter des données de test dans `app.db`.
- [ ] **Vérification finale :** S'assurer que tous les livrables sont présents.

---

## Intégrité des Données (Spécifications)
- **Email unique** pour les utilisateurs.
- **Capacité de session >= 1**.
- **Date de fin > Date de début** pour les sessions.
- **Un apprenant ne peut s'inscrire qu'une fois par session.**
- **Contrôle de la capacité maximale** lors de l'inscription.
