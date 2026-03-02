# Détails de l'Implémentation du Projet — Simplon Manage API

Ce document détaille la structure, les étapes d'implémentation et la stratégie de qualité du projet Simplon Manage API.

## 1. Présentation du Projet
Simplon Manage API est une application RESTful conçue pour automatiser la gestion d'un centre de formation. Elle permet de gérer les **Formations**, les **Sessions**, les **Utilisateurs** et les **Inscriptions**.

## 2. Architecture Technique
Le projet suit une architecture inspirée par les principes de la **Clean Architecture**, séparant les responsabilités en plusieurs couches :

- **Models (`app/models/`)** : Définition des entités de la base de données via SQLAlchemy (Structure des données).
- **Schemas (`app/schemas/`)** : Modèles de validation Pydantic pour les requêtes (Input) et les réponses (Output).
- **Services (`app/services/`)** : Couche "Métier" contenant toute la logique décisionnelle, les calculs et les validations complexes.
- **Routes (`app/routes/`)** : Points d'entrée de l'API (Endpoints) gérant les requêtes HTTP.

## 3. Étapes d'Implémentation
Le développement s'est déroulé en plusieurs phases clés :

1.  **Initialisation** : Mise en place de l'environnement, installation de FastAPI et configuration de SQLAlchemy avec SQLite.
2.  **Modélisation Core** : Création des modèles `User`, `Formation` et `Session`.
3.  **Gestion des Sessions** : Implémentation de la logique de création et mise à jour des sessions avec validation des dates (début < fin).
4.  **Système d'Inscriptions** : Développement de la logique d'inscription connectant les utilisateurs aux sessions, avec gestion des capacités maximales.
5.  **Refactorisation (Logic Layer)** : Migration de la logique critique des schemas vers les services pour une meilleure robustesse.
6.  **Pagination** : Ajout de la pagination sur les routes de liste (ex: `/inscriptions/`) pour gérer de gros volumes de données.

## 4. Fonctionnalités Clés
- **Validation Intelligente** : Empêche l'inscription d'un utilisateur à une session complète.
- **Gestion d'État** : Archivage automatique ou manuel des sessions selon leur statut.
- **Découplage** : Utilisation de DTO (Data Transfer Objects) via Pydantic pour masquer les détails de la base de données.

## 5. Stratégie de Tests
La qualité du code est assurée par une suite de tests automatisés située dans le dossier `/tests` :

- **Tests unitaires (`test_users.py`, `test_formations.py`)** : Vérifient que chaque petite brique de code (une fonction de service, par exemple) fonctionne de manière isolée.
- **Tests d'intégrité (`test_integrity.py`)** : S'assurent que les différentes parties du système communiquent correctement entre elles (ex: l'ajout d'une inscription met-il bien à jour la capacité restante de la session ?).
- **Tests de validation** : Vérifient que les contraintes métiers (dates, doublons, formats d'email) sont strictement respectées.

Chaque test sert de **documentation exécutable** et garantit que les futures modifications ne casseront pas l'existant.
