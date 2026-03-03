const API_BASE_URL = typeof window !== 'undefined' 
  ? (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000")
  : "http://127.0.0.1:8000";

console.log("Connecting to API at:", API_BASE_URL);

// --- Types based on Pydantic Schemas ---

export interface User {
  id: number;
  email: string;
  surname: string;
  name: string;
  birth_date: string;
  role: "Etudiant" | "Formateur" | "Administrateur";
  inscription_date: string;
  is_active: boolean;
}

export interface Formation {
  id: number;
  title: string;
  description: string;
  duration: number;
  level: "débutant" | "intermédiaire" | "avancé";
  created_at: string;
  updated_at: string;
}

export interface Session {
  id: number;
  formation_id: number;
  formateur_id: number;
  date_debut: string;
  date_fin: string;
  capacite_max: number;
  statut: "planifiée" | "en_cours" | "terminée" | "annulée";
  nombre_inscrits: number;
  formation?: Formation;
  formateur?: User;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

// --- API Functions ---

async function handleResponse<T>(response: Response): Promise<T> {
  if (response.status === 204) return {} as T;
  if (!response.ok) {
    let errorDetail = response.statusText;
    try {
      const error = await response.json();
      errorDetail = error.detail || JSON.stringify(error) || response.statusText;
    } catch {
      // Not a JSON error
    }
    console.error(`API Error (${response.status}):`, errorDetail);
    throw new Error(errorDetail);
  }
  const data = await response.json();
  return data as T;
}

// Formations
export const fetchFormations = (page = 1, size = 10): Promise<PaginatedResponse<Formation>> =>
  fetch(`${API_BASE_URL}/formations/?page=${page}&size=${size}`).then(res => handleResponse<PaginatedResponse<Formation>>(res));

export const createFormation = (data: Partial<Formation>): Promise<Formation> =>
  fetch(`${API_BASE_URL}/formations/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<Formation>(res));

export const updateFormation = (id: number, data: Partial<Formation>): Promise<Formation> =>
  fetch(`${API_BASE_URL}/formations/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<Formation>(res));

export const deleteFormation = (id: number): Promise<void> =>
  fetch(`${API_BASE_URL}/formations/${id}`, { method: "DELETE" }).then(res => handleResponse<void>(res));

// Users (prefix /utilisateurs)
export const fetchUsers = (page = 1, size = 10, activeOnly = false): Promise<PaginatedResponse<User>> =>
  fetch(`${API_BASE_URL}/utilisateurs/?page=${page}&size=${size}&active_only=${activeOnly}`).then(res => handleResponse<PaginatedResponse<User>>(res));

export const createUser = (data: Partial<User>): Promise<User> =>
  fetch(`${API_BASE_URL}/utilisateurs/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<User>(res));

export const updateUser = (id: number, data: Partial<User>): Promise<User> =>
  fetch(`${API_BASE_URL}/utilisateurs/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<User>(res));

export const deleteUser = (id: number): Promise<void> =>
  fetch(`${API_BASE_URL}/utilisateurs/${id}`, { method: "DELETE" }).then(res => handleResponse<void>(res));

// Sessions
export const fetchSessions = (page = 1, size = 10): Promise<PaginatedResponse<Session>> =>
  fetch(`${API_BASE_URL}/sessions/?page=${page}&size=${size}`).then(res => handleResponse<PaginatedResponse<Session>>(res));

export const fetchSessionDetails = (id: number): Promise<Session> =>
  fetch(`${API_BASE_URL}/sessions/${id}`).then(res => handleResponse<Session>(res));

export const createSession = (data: Partial<Session>): Promise<Session> =>
  fetch(`${API_BASE_URL}/sessions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<Session>(res));

export const updateSession = (id: number, data: Partial<Session>): Promise<Session> =>
  fetch(`${API_BASE_URL}/sessions/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<Session>(res));

export const deleteSession = (id: number): Promise<void> =>
  fetch(`${API_BASE_URL}/sessions/${id}`, { method: "DELETE" }).then(res => handleResponse<void>(res));

// Inscriptions
export const fetchInscriptionsBySession = (sessionId: number): Promise<any> =>
  fetch(`${API_BASE_URL}/inscriptions/session/${sessionId}`).then(res => handleResponse<any>(res));

export const createInscription = (data: { user_id: number; session_id: number }): Promise<any> =>
  fetch(`${API_BASE_URL}/inscriptions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(res => handleResponse<any>(res));
