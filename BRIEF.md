# Brief Métier : API de gestion pour un centre de formation

**Technologies :** FastAPI • DTOs • Validation • Tests automatisés  
**Durée :** 8 jours  

---

## Contexte Professionnel

Vous êtes développeur·euse backend dans une ESN spécialisée dans les solutions métiers.

Votre client, **Simplon**, est un centre de formation qui souhaite digitaliser la gestion de :
- ses apprenants,
- ses formateurs,
- ses sessions de formation.

### Situation actuelle

- Les inscriptions sont gérées via tableurs  
- Le suivi pédagogique est dispersé  
- La gestion des sessions est difficile  

### Mission

Concevoir une **API REST professionnelle** permettant de gérer :

- les formations  
- les sessions  
- les inscriptions  

En respectant les standards modernes :

- architecture claire  
- DTOs & validation robuste  
- tests automatisés  
- documentation exploitable  

---

## Modalités pédagogiques

- Travail en équipe projet (méthode Agile simplifiée)  
- Mise en pratique des bonnes pratiques backend  
- Revues de code régulières  
- Soutenance finale avec présentation technique  

---

## Organisation & Planning

### Jour 1–2
- Setup projet & architecture  
- Modélisation des entités  
- DTOs & validation Pydantic  

### Jour 3–5
- CRUD principaux  
- Relations entre entités  
- Règles métier  

### Jour 6–7
- Tests automatisés  
- Gestion des erreurs  
- Filtres & pagination  

### Jour 8
- Finalisation  
- Documentation  
- Soutenance  

---

# Besoins à Réaliser

## 1️⃣ Fonctionnalités Obligatoires

---

## Gestion des utilisateurs

**CRUD complet**

### Types d’utilisateurs :
- administrateur  
- formateur  
- apprenant  

### Champs :
- nom  
- prénom  
- email (unique)  
- rôle  
- date d’inscription  

### Contraintes :
- email valide et unique  
- rôle obligatoire  

---

## Gestion des formations

**CRUD complet**

### Champs :
- titre  
- description  
- durée (heures)  
- niveau (débutant, intermédiaire, avancé)  

### Contraintes :
- durée > 0  
- titre obligatoire  

---

## Gestion des sessions de formation

**CRUD complet**

### Champs :
- formation associée  
- formateur  
- date de début  
- date de fin  
- capacité maximale  

### Contraintes :
- date fin > date début  
- capacité ≥ 1  

---

## Gestion des inscriptions

Permet d’inscrire un apprenant à une session.

### Endpoints :
- inscrire un apprenant  
- lister les inscrits d’une session  
- lister les sessions d’un apprenant  
- désinscrire un apprenant  

### Contraintes :
- capacité maximale respectée  
- un apprenant ne peut être inscrit qu’une fois par session  
- session existante obligatoire  

---

# Validation & Intégrité des données

Utilisation de **Pydantic v2** :

- DTOs distincts (Create / Update / Read)  
- validateurs personnalisés  
- normalisation des données  

### Exemples de règles :
- email valide  
- dates cohérentes  
- durée positive  
- capacité non dépassée  

---

# Challenge Technique

## Architecture & Bonnes pratiques

- séparation modèles / schémas / services / routes  
- DTOs pour les entrées/sorties  
- gestion centralisée des erreurs  
- pagination & filtres  
- gestion cohérente des statuts HTTP  

## Base de données

- SQLModel ou SQLAlchemy ORM  
- migrations avec Alembic  

## Documentation

- documentation Swagger automatique  
- description claire des endpoints  

---

# Tests Automatisés (obligatoire)

- pytest  
- tests des endpoints principaux  
- tests des règles métier  
- tests des cas d’erreurs  

**Couverture recommandée : ≥ 70%**

---

# Fonctionnalités Bonus

## 🔹 Bonus API

- recherche filtrée (dates, formateur, niveau)  
- pagination avancée  
- tri des résultats  
- statut session (planifiée, en cours, terminée)  

## 🔹 Bonus métier

- liste d’attente automatique si session complète  
- statistiques simples :
  - nombre d’apprenants par formation  
  - taux de remplissage  

## 🔹 Bonus technique

- fixtures de test avancées  
- seed automatique de données  
- logging structuré  

---

# Livrables

| # | Livrable |
|---|----------|
| 1 | Code source sur Git (structure propre) |
| 2 | README.md clair et documenté |
| 3 | Documentation Swagger/OpenAPI |
| 4 | Scripts migrations Alembic |
| 5 | Suite de tests automatisés |
| 6 | Slides de présentation (architecture & démonstration) |

---

# Critères de Performance

## Fonctionnalités & Qualité

- CRUD complets opérationnels  
- respect des règles métier  
- validation robuste des données  
- gestion claire des erreurs  

## Qualité technique

- architecture propre et lisible  
- DTOs bien structurés  
- cohérence des statuts HTTP  
- couverture de tests ≥ 70%  

## Documentation & Collaboration

- README clair et exploitable  
- documentation des endpoints  
- utilisation efficace de Git  

## Respect du calendrier

- jalons respectés  
- démonstration fonctionnelle finale  

---

# Ressources

- FastAPI  
- Pydantic v2  
- SQLModel / SQLAlchemy  
- Alembic  
- Pytest  
- Swagger / OpenAPI  
