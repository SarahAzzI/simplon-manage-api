/**
 * C'est ici que nous définissons comment le Frontend parle au Backend (votre API FastAPI).
 * 
 * En React/Next.js, on utilise souvent 'fetch' ou des bibliothèques comme 'SWR' ou 'React Query'.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchStats() {
    const response = await fetch(`${API_BASE_URL}/stats/fill-rate`);
    if (!response.ok) throw new Error("Erreur lors de la récupération des stats");
    return response.json();
}

export async function fetchSessions() {
    const response = await fetch(`${API_BASE_URL}/sessions/`);
    if (!response.ok) throw new Error("Erreur lors de la récupération des sessions");
    return response.json();
}

/**
 * EXPLICATION POUR AMAURY :
 * 
 * 1. 'use client' : En haut de page.tsx, cela indique que le composant est interactif.
 * 2. 'useEffect' : On utilise ce "Hook" pour appeler ces fonctions au chargement de la page.
 * 3. 'useState' : On stocke les données reçues de FastAPI dans une "variable d'état" pour que React mette à jour l'écran automatiquement.
 */
