# Documentation Technique : Simplon Manage API

Ce document explique l'architecture du projet, son fonctionnement interne et les étapes de son implémentation.

## 1. Architecture Logicielle
Le projet suit une architecture en couches pour séparer les responsabilités :

### 📡 Couche Routes (`app/routes/`) - "Le Guichet"
C'est le point d'entrée de l'API.
*   **Rôle** : Reçoit les requêtes HTTP, définit les URL (endpoints) et appelle les services.
*   **Technologie** : FastAPI.

### 📝 Couche Schémas (`app/schemas/`) - "Le Contrat"
Définit la structure des données qui entrent et sortent de l'API.
*   **Rôle** : Valide le format des données (ex: email valide, longueur minimale des textes).
*   **Technologie** : Pydantic.

### ⚙️ Couche Services (`app/services/`) - "Le Cerveau"
Contient toute la logique métier. **C'est ici que le travail réel est fait.**
*   **Rôle** : Effectue les calculs, vérifie les règles complexes (ex: "une session ne peut pas finir avant de commencer") et interagit avec la base de données.

### 🗄️ Couche Modèles (`app/models/`) - "La Mémoire"
Représente la structure physique des tables en base de données.
*   **Rôle** : Définit les colonnes, les types de données et les relations entre les tables.
*   **Technologie** : SQLAlchemy.

---

## 2. Fonctionnement Interne (Flux de données)
Quand tu appelles une URL (ex: `POST /sessions/`) :
1.  **Route** : Reçoit le JSON.
2.  **Schéma** : Vérifie que le JSON a le bon format.
3.  **Service** : Vérifie si la formation existe, si le formateur a le bon rôle, calcule les dates.
4.  **Modèle** : Enregistre les données dans le fichier `app.db`.
5.  **Réponse** : Le service renvoie l'objet créé à la route, qui le transforme en JSON via un schéma de réponse.

---

## 3. Étapes d'Implémentation
Le projet a été construit de manière itérative :

1.  **Fondation** : Mise en place de FastAPI et de la connexion à la base de données SQLite.
2.  **Utilisateurs & Formations** : Création des premiers CRUD (Create, Read, Update, Delete).
3.  **Inscriptions** : Mise en place de la table de liaison pour permettre aux étudiants de s'inscrire à des sessions.
4.  **Refactoring Session (Étape actuelle)** : 
    *   Ajout du cycle de vie des sessions (statuts).
    *   Renforcement de la sécurité des données (validations).
    *   Mise en place de tests automatisés pour atteindre une couverture de code maximale (>95%).
5.  **Migrations** : Utilisation d'Alembic pour gérer les évolutions de la base de données sans perdre de données.

---

## 4. "Qui fait quoi" (Résumé des composants)
*   **FastAPI** : S'occupe du serveur web et de la documentation automatique (Swagger).
*   **SQLAlchemy** : Traduit le code Python en requêtes SQL.
*   **Alembic** : Historique des changements de la base de données.
*   **Pytest** : S'assure que chaque nouvelle modification ne casse pas l'existant.
