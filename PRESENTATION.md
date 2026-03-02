# Présentation Technique : Simplon Manage API

Ce fichier définit la structure d'une présentation technique en 12 slides.

---

## Slide 1 : Titre & Introduction
- **Titre** : Simplon Manage API
- **Sous-titre** : Moderniser la gestion des centres de formation
- **Points clés** : Présentation de l'intervenant et contexte du projet.

## Slide 2 : Le Problème
- **Problématique** : Gestion manuelle des inscriptions, erreurs de saisie sur les dates, dépassement des capacités des salles.
- **Besoin** : Une solution automatisée, fiable et scalable.

## Slide 3 : La Solution : Simplon Manage API
- **Concept** : Une API REST robuste pour centraliser les données.
- **Objectifs** : Fiabilité des données, automatisation des processus métiers, interface claire pour les futurs front-ends.

## Slide 4 : Stack Technique
- **Framework** : FastAPI (Performance, Typage Python).
- **Base de données** : SQLAlchemy (ORM) & SQLite.
- **Validation** : Pydantic (Sécurité des données).

## Slide 5 : Architecture Logicielle
- **Pattern** : Service-Repository Pattern.
- **Pourquoi ?** : Séparation des tâches. La route reçoit l'appel, le service décide de la règle métier, le modèle gère la donnée.

## Slide 6 : Gestion des Formations & Sessions
- **Concepts** : Lien 1-N entre Formation et Session.
- **Règle Métier** : Une session doit obligatoirement avoir une date de début antérieure à sa date de fin.

## Slide 7 : Inscriptions & Utilisateurs
- **Concepts** : Association entre un Utilisateur et une Session.
- **Contrainte Critique** : Validation automatique de la capacité maximale de la session avant d'accepter une inscription.

## Slide 8 : Assurance Qualité (Tests)
- **Approche** : Test-Driven Development (TDD) partiel.
- **Objectif** : 0 régression. Chaque bug trouvé devient un test pour ne plus jamais réapparaître.

## Slide 9 : Focus : Tests d'Intégrité
- **C'est quoi ?** Tester le flux complet (Create -> Read -> Update -> Delete).
- **Utilité** : Garantir que la base de données reste cohérente après des opérations complexes.

## Slide 10 : Défis Rencontrés & Solutions
- **Défi** : Centraliser la validation sans dupliquer le code.
- **Solution** : Migration de la logique des schemas vers une couche Service unifiée.

## Slide 11 : Évolutions Futures
- **Roadmap** :
  - Authentification JWT (Sécurité).
  - Export PDF des attestations.
  - Interface Dashboard (React/Next.js).

## Slide 12 : Conclusion & Questions
- **Résumé** : Une API prête pour la production, testée et documentée.
- **Contact** : [Votre Nom/Email]
- **Merci pour votre attention !**
