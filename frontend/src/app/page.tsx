"use client";

import React, { useState, useEffect } from "react";
import {
  Users,
  GraduationCap,
  Calendar,
  Settings,
  BarChart3,
  LayoutDashboard,
  Plus,
  ArrowUpRight,
  Search,
  BookOpen,
  UserCheck,
  MoreVertical,
  ChevronRight
} from "lucide-react";

import { StatsChart } from "@/components/stats-chart";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { 
  fetchUsers, 
  fetchFormations, 
  fetchSessions,
  deleteUser,
  deleteFormation,
  deleteSession,
  createFormation,
  createUser,
  createSession,
  updateFormation,
  updateUser,
  updateSession,
  User,
  Formation,
  Session
} from "@/lib/api";

interface SidebarLinkProps {
  icon: React.ElementType;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

type ViewType = 'dashboard' | 'formations' | 'sessions' | 'utilisateurs' | 'stats' | 'settings';

export default function DashboardPage() {
  const [view, setView] = useState<ViewType>('dashboard');
  const [data, setData] = useState<{
    users: User[],
    formations: Formation[],
    sessions: Session[],
    totalUsers: number,
    totalFormations: number,
    totalSessions: number,
  }>({
    users: [],
    formations: [],
    sessions: [],
    totalUsers: 0,
    totalFormations: 0,
    totalSessions: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [usersRes, formationsRes, sessionsRes] = await Promise.all([
        fetchUsers(1, 100),
        fetchFormations(1, 100),
        fetchSessions(1, 100),
      ]);
      
      setData({
        users: usersRes.items || [],
        formations: formationsRes.items || [],
        sessions: sessionsRes.items || [],
        totalUsers: usersRes.total || 0,
        totalFormations: formationsRes.total || 0,
        totalSessions: sessionsRes.total || 0,
      });
    } catch (err) {
      console.error("Failed to fetch data:", err);
      const message = err instanceof Error ? err.message : String(err);
      setError(message || "Impossible de se connecter à l'API. Vérifiez que le backend est lancé.");
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = () => {
    const totalStudents = data.users.filter(u => u.role === 'Etudiant').length;
    const activeFormations = data.formations.length;
    const upcomingSessions = data.sessions.filter(s => new Date(s.date_debut) > new Date()).length;
    
    // Fill rate calculation
    const totalCapacity = data.sessions.reduce((acc, s) => acc + s.capacite_max, 0);
    const totalInscriptions = data.sessions.reduce((acc, s) => acc + s.nombre_inscrits, 0);
    const fillRate = totalCapacity > 0 ? Math.round((totalInscriptions / totalCapacity) * 100) : 0;

    return [
      { name: "Total Étudiants", value: totalStudents.toString(), icon: Users, color: "text-[#CE0033]", bg: "bg-[#CE0033]/10", trend: totalStudents > 0 ? "Actif" : "Aucun" },
      { name: "Formations Actives", value: activeFormations.toString(), icon: BookOpen, color: "text-zinc-900 dark:text-white", bg: "bg-zinc-100 dark:bg-zinc-800", trend: activeFormations > 0 ? "En ligne" : "À créer" },
      { name: "Sessions à venir", value: upcomingSessions.toString(), icon: Calendar, color: "text-[#CE0033]", bg: "bg-[#CE0033]/5", trend: upcomingSessions > 0 ? "Planifiées" : "Aucune" },
      { name: "Taux de remplissage", value: `${fillRate}%`, icon: BarChart3, color: "text-green-600", bg: "bg-green-50", trend: "Moyenne" },
    ];
  };

  const chartData = React.useMemo(() => {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const currentYear = new Date().getFullYear();
    const monthlyData = months.map(m => ({ name: m, total: 0 }));

    data.sessions.forEach(s => {
      const date = new Date(s.date_debut);
      if (date.getFullYear() === currentYear) {
        monthlyData[date.getMonth()].total += 1; // Count sessions per month
      }
    });

    return monthlyData.slice(0, 7); // Show last 7 months for better UX
  }, [data.sessions]);

  const statsList = calculateStats();


  // --- Modals State ---
  const [isFormationModalOpen, setIsFormationModalOpen] = useState(false);
  const [newFormation, setNewFormation] = useState({
    title: "",
    description: "",
    duration: 450,
    level: "débutant" as Formation['level']
  });

  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [newUser, setNewUser] = useState({
    email: "",
    name: "",
    surname: "",
    birth_date: new Date().toISOString().split('T')[0],
    role: "Etudiant" as User['role']
  });

  const [isSessionModalOpen, setIsSessionModalOpen] = useState(false);
  const [newSession, setNewSession] = useState({
    formation_id: 0,
    formateur_id: 0,
    date_debut: new Date().toISOString().split('T')[0],
    date_fin: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    capacite_max: 20
  });

  // --- Handlers ---
  const [editingFormation, setEditingFormation] = useState<Formation | null>(null);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [editingSession, setEditingSession] = useState<Session | null>(null);
  
  const handleUpdateFormation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingFormation) return;
    try {
      await updateFormation(editingFormation.id, editingFormation);
      setEditingFormation(null);
      loadData();
    } catch (error) {
      alert("Erreur: " + error);
    }
  };

  const handleUpdateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingUser) return;
    try {
      await updateUser(editingUser.id, editingUser);
      setEditingUser(null);
      loadData();
    } catch (error) {
      alert("Erreur: " + error);
    }
  };

  const handleUpdateSession = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingSession) return;
    try {
      await updateSession(editingSession.id, editingSession);
      setEditingSession(null);
      loadData();
    } catch (error) {
      alert("Erreur: " + error);
    }
  };

  const handleCreateFormation = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createFormation(newFormation);
      setIsFormationModalOpen(false);
      loadData();
    } catch (error) {
      alert("Erreur: " + error);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createUser(newUser);
      setIsUserModalOpen(false);
      loadData();
    } catch (error) {
      alert("Erreur: " + error);
    }
  };

  const handleCreateSession = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSession.formation_id || !newSession.formateur_id) {
      alert("Veuillez sélectionner une formation et un formateur.");
      return;
    }
    try {
      await createSession(newSession);
      setIsSessionModalOpen(false);
      loadData();
    } catch (error) {
      alert("Erreur: " + error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const calculateFillPercentage = (current: number, total: number) => {
    if (!total) return 0;
    return (current / total) * 100;
  };

  const renderDashboard = () => (
    <>
      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        {statsList.map((stat, i) => (
          <Card key={i} className="border-none shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden glass-card hover:-translate-y-1">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400 mb-1">{stat.name}</p>
                  <h3 className="text-3xl font-bold text-zinc-900 dark:text-zinc-50">{loading ? "..." : stat.value}</h3>
                </div>
                <div className={`${stat.bg} ${stat.color} p-4 rounded-2xl group-hover:scale-110 transition-transform duration-500`}>
                  <stat.icon size={26} />
                </div>
              </div>
              <div className="mt-4 flex items-center text-xs text-green-600 font-bold tracking-tight">
                <ArrowUpRight size={14} className="mr-1" />
                <span>{stat.trend}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <Card className="xl:col-span-2 border-none shadow-sm glass-card overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between p-8 pb-4">
            <div>
              <CardTitle className="text-2xl font-bold">Prochaines Sessions</CardTitle>
              <CardDescription className="text-zinc-500">Aperçu rapide des formations imminentes.</CardDescription>
            </div>
            <Button variant="outline" className="rounded-full border-[#CE0033] text-[#CE0033] hover:bg-[#CE0033] hover:text-white transition-colors" onClick={() => setView('sessions')}>
              Voir tout
            </Button>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent border-zinc-100/50 dark:border-zinc-800">
                  <TableHead className="pl-8 font-bold text-zinc-400 uppercase text-[10px] tracking-widest">Formation</TableHead>
                  <TableHead className="font-bold text-zinc-400 uppercase text-[10px] tracking-widest text-center">Date Début</TableHead>
                  <TableHead className="font-bold text-zinc-400 uppercase text-[10px] tracking-widest text-center">Capacité</TableHead>
                  <TableHead className="font-bold text-zinc-400 uppercase text-[10px] tracking-widest text-center">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow><TableCell colSpan={4} className="text-center py-16 text-zinc-400 text-sm italic">Synchronisation avec Simplon API...</TableCell></TableRow>
                ) : data.sessions.length === 0 ? (
                  <TableRow><TableCell colSpan={4} className="text-center py-16 text-zinc-400 text-sm">Aucune session active actuellement.</TableCell></TableRow>
                ) : data.sessions.slice(0, 5).map((session) => (
                  <TableRow key={session.id} className="group border-zinc-50/50 dark:border-zinc-800/50 hover:bg-zinc-50/80 dark:hover:bg-zinc-800/30 transition-all cursor-pointer">
                    <TableCell className="pl-8 py-5">
                      <div className="font-bold text-zinc-900 dark:text-zinc-100 group-hover:text-[#CE0033] transition-colors">{session.formation?.title || "Session Spéciale"}</div>
                      <div className="flex items-center gap-2 mt-1">
                        <UserCheck size={12} className="text-[#CE0033]" />
                        <span className="text-xs text-zinc-500 font-medium">{session.formateur?.name} {session.formateur?.surname}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-center font-medium text-zinc-600 dark:text-zinc-400">{new Date(session.date_debut).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}</TableCell>
                    <TableCell className="text-center">
                      <div className="flex flex-col items-center gap-2">
                        <span className="text-xs font-bold text-zinc-900 dark:text-zinc-100">{session.nombre_inscrits} / {session.capacite_max}</span>
                        <div className="w-24 h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-[#CE0033] rounded-full transition-all duration-1000 ease-out shadow-[0_0_8px_rgba(206,0,51,0.5)]"
                            style={{ width: `${calculateFillPercentage(session.nombre_inscrits, session.capacite_max)}%` }}
                          ></div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-center pr-8">
                      <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider
                        ${new Date(session.date_debut) > new Date() ? 'bg-blue-50 text-blue-600' : 'bg-red-50 text-[#CE0033]'}`}>
                        {new Date(session.date_debut) > new Date() ? 'Soon' : 'Live'}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <div className="space-y-8">
          <Card className="border-none shadow-sm glass-card">
            <CardHeader>
              <CardTitle className="text-xl font-bold">Activité</CardTitle>
              <CardDescription>Inscriptions sur le semestre.</CardDescription>
            </CardHeader>
            <CardContent className="pb-8">
              <StatsChart data={chartData} />
            </CardContent>
          </Card>

          <Card className="border-none shadow-xl bg-gradient-to-br from-[#CE0033] to-[#E6003A] text-white overflow-hidden relative group">
            <div className="absolute -top-10 -right-10 p-4 opacity-10 group-hover:scale-110 transition-transform duration-700">
              <GraduationCap size={200} />
            </div>
            <CardHeader className="relative z-10">
              <CardTitle className="text-2xl font-black italic tracking-tighter uppercase">Simplon Network</CardTitle>
              <CardDescription className="text-red-100 font-medium">Connecté au Cloud Simplon.</CardDescription>
            </CardHeader>
            <CardContent className="relative z-10">
              <p className="text-sm mb-6 text-red-50 leading-relaxed">Gérez vos formations et administrez vos sessions IA avec une précision chirurgicale.</p>
              <Button variant="secondary" className="w-full rounded-2xl font-bold py-6 bg-white text-[#CE0033] hover:bg-zinc-100 shadow-lg transition-all active:scale-95" onClick={() => setView('utilisateurs')}>
                ACCES ADMINISTRATEURS
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );

  const renderFormations = () => (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-4xl font-black tracking-tighter text-zinc-900 dark:text-zinc-50 uppercase italic">Catalogue Formations</h2>
          <p className="text-zinc-500 mt-2">Explorez nos parcours certifiants et innovants.</p>
        </div>
        <Button 
          className="bg-[#CE0033] hover:bg-[#B3002D] rounded-full px-6 py-6 shadow-lg shadow-red-500/20"
          onClick={() => setIsFormationModalOpen(true)}
        >
          <Plus size={20} className="mr-2" /> AJOUTER UNE FORMATION
        </Button>
      </div>

      {isFormationModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-zinc-950 w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-zinc-900 animate-in zoom-in-95 duration-200">
            <h3 className="text-2xl font-black uppercase italic mb-6">Nouvelle Formation</h3>
            <form onSubmit={handleCreateFormation} className="space-y-4">
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Titre de la formation</label>
                <input 
                  required
                  value={newFormation.title}
                  onChange={e => setNewFormation({...newFormation, title: e.target.value})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Description</label>
                <textarea 
                  required
                  rows={3}
                  value={newFormation.description}
                  onChange={e => setNewFormation({...newFormation, description: e.target.value})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Durée (Mois)</label>
                  <input 
                    type="number"
                    value={newFormation.duration}
                    onChange={e => setNewFormation({...newFormation, duration: parseInt(e.target.value)})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Niveau</label>
                  <select 
                    value={newFormation.level}
                    onChange={e => setNewFormation({...newFormation, level: e.target.value as Formation['level']})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  >
                    <option value="Bac+2">Bac+2</option>
                    <option value="Bac+3">Bac+3</option>
                    <option value="Bac+5">Bac+5</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-4 mt-8">
                <Button variant="ghost" className="flex-1 rounded-xl" onClick={() => setIsFormationModalOpen(false)}>ANNULER</Button>
                <Button type="submit" className="flex-1 bg-[#CE0033] text-white rounded-xl">ENREGISTRER</Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {editingFormation && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-zinc-950 w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-zinc-900 animate-in zoom-in-95 duration-200">
            <h3 className="text-2xl font-black uppercase italic mb-6">Éditer Formation</h3>
            <form onSubmit={handleUpdateFormation} className="space-y-4">
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Titre</label>
                <input 
                  required
                  value={editingFormation.title}
                  onChange={e => setEditingFormation({...editingFormation, title: e.target.value})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Description</label>
                <textarea 
                  required
                  rows={3}
                  value={editingFormation.description}
                  onChange={e => setEditingFormation({...editingFormation, description: e.target.value})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Durée</label>
                  <input 
                    type="number"
                    value={editingFormation.duration}
                    onChange={e => setEditingFormation({...editingFormation, duration: parseInt(e.target.value)})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Niveau</label>
                  <select 
                    value={editingFormation.level}
                    onChange={e => setEditingFormation({...editingFormation, level: e.target.value as Formation['level']})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  >
                    <option value="Bac+2">Bac+2</option>
                    <option value="Bac+3">Bac+3</option>
                    <option value="Bac+5">Bac+5</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-4 mt-8">
                <Button variant="ghost" className="flex-1 rounded-xl" onClick={() => setEditingFormation(null)}>ANNULER</Button>
                <Button type="submit" className="flex-1 bg-black text-white dark:bg-white dark:text-black rounded-xl">ENREGISTRER</Button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {data.formations.map((formation) => (
          <Card key={formation.id} className="border-none glass-card hover:shadow-2xl transition-all duration-500 group overflow-hidden hover:-translate-y-2">
            <div className="h-32 bg-gradient-to-br from-[#CE0033] to-zinc-900 p-6 relative">
              <div className="absolute bottom-4 left-6 text-white font-black text-xl uppercase italic group-hover:scale-105 transition-transform">{formation.title}</div>
              <GraduationCap className="absolute top-4 right-4 text-white/20 group-hover:rotate-12 transition-transform" size={48} />
            </div>
            <CardContent className="p-8">
              <div className="flex items-center gap-3 mb-4">
                <span className="bg-black text-white text-[10px] font-black px-3 py-1 rounded-full uppercase tracking-tighter">{formation.level || "Expert"}</span>
                <span className="text-zinc-400 text-xs font-bold">{formation.duration || 450} MOIS</span>
              </div>
              <p className="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed mb-8 line-clamp-3">
                {formation.description}
              </p>
                <div className="flex gap-2">
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="flex-1 rounded-xl border border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all font-bold text-[10px] tracking-tight"
                    onClick={() => setEditingFormation(formation)}
                  >
                    ÉDITER
                  </Button>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="flex-1 rounded-xl border border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all font-bold text-[10px] tracking-tight text-red-500 hover:text-red-600"
                    onClick={async () => {
                      if(confirm("Supprimer cette formation ?")) {
                        await deleteFormation(formation.id);
                        loadData();
                      }
                    }}
                  >
                    SUPPRIMER
                  </Button>
                </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );

  const renderSessions = () => (
    <Card className="border-none glass-card overflow-hidden animate-in zoom-in-95 duration-500">
       <CardHeader className="p-10 pb-6 flex flex-row items-center justify-between bg-zinc-50/30 dark:bg-zinc-900/10">
        <div>
          <CardTitle className="text-3xl font-black italic tracking-tighter uppercase">Planification Sessions</CardTitle>
          <CardDescription>Vue détaillée de la logistique pédagogique ({data.totalSessions}).</CardDescription>
        </div>
        <div className="flex gap-4">
           <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" size={16} />
              <input type="text" placeholder="Filtrer..." className="pl-10 pr-4 py-2 rounded-full border border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 outline-none focus:ring-2 focus:ring-[#CE0033]/20 transition-all w-48" />
           </div>
           <Button 
             className="bg-black dark:bg-white dark:text-black text-white rounded-full"
             onClick={() => setIsSessionModalOpen(true)}
           >
             NOUVELLE SESSION
           </Button>
        </div>
      </CardHeader>

      {isSessionModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-zinc-950 w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-zinc-900 animate-in zoom-in-95 duration-200">
            <h3 className="text-2xl font-black uppercase italic mb-6">Nouvelle Session</h3>
            <form onSubmit={handleCreateSession} className="space-y-4">
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Formation</label>
                <select 
                  required
                  value={newSession.formation_id}
                  onChange={e => setNewSession({...newSession, formation_id: parseInt(e.target.value)})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                >
                  <option value={0}>Sélectionner une formation</option>
                  {data.formations.map(f => (
                    <option key={f.id} value={f.id}>{f.title}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Formateur Référent</label>
                <select 
                  required
                  value={newSession.formateur_id}
                  onChange={e => setNewSession({...newSession, formateur_id: parseInt(e.target.value)})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                >
                  <option value={0}>Sélectionner un formateur</option>
                  {data.users.filter(u => u.role === 'Formateur').map(u => (
                    <option key={u.id} value={u.id}>{u.name} {u.surname}</option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Date Debut</label>
                  <input 
                    type="date"
                    required
                    value={newSession.date_debut}
                    onChange={e => setNewSession({...newSession, date_debut: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Date Fin</label>
                  <input 
                    type="date"
                    required
                    value={newSession.date_fin}
                    onChange={e => setNewSession({...newSession, date_fin: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
              </div>
              <div className="flex gap-4 mt-8">
                <Button variant="ghost" className="flex-1 rounded-xl" onClick={() => setIsSessionModalOpen(false)}>ANNULER</Button>
                <Button type="submit" className="flex-1 bg-[#CE0033] text-white rounded-xl">PLANIFIER</Button>
              </div>
            </form>
          </div>
        </div>
      )}
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow className="border-zinc-100 dark:border-zinc-800">
               <TableHead className="pl-10 font-black uppercase text-[10px] tracking-[0.2em] text-zinc-400">Période</TableHead>
               <TableHead className="font-black uppercase text-[10px] tracking-[0.2em] text-zinc-400">Intitulé Formation</TableHead>
               <TableHead className="font-black uppercase text-[10px] tracking-[0.2em] text-zinc-400">Formateur Référent</TableHead>
               <TableHead className="text-center font-black uppercase text-[10px] tracking-[0.2em] text-zinc-400">Occupation</TableHead>
               <TableHead className="text-right pr-10"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.sessions.map((session) => (
              <TableRow key={session.id} className="hover:bg-zinc-50/50 dark:hover:bg-zinc-800/20 border-zinc-50 dark:border-zinc-900 group">
                <TableCell className="pl-10 py-6">
                  <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">{new Date(session.date_debut).toLocaleDateString('fr-FR')}</div>
                  <div className="text-[10px] text-zinc-400 font-bold tracking-tighter">FIN : {new Date(session.date_fin).toLocaleDateString('fr-FR')}</div>
                </TableCell>
                <TableCell className="py-6">
                  <div className="font-black uppercase italic text-zinc-600 dark:text-zinc-300 group-hover:text-[#CE0033] transition-colors">{session.formation?.title || "MODULE EXTERNE"}</div>
                </TableCell>
                <TableCell className="py-6">
                  <div className="flex items-center gap-3">
                    <div className="size-8 rounded-full bg-[#CE0033] flex items-center justify-center text-white text-[10px] font-bold">
                       {session.formateur?.name?.[0]}{session.formateur?.surname?.[0]}
                    </div>
                    <div>
                      <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">{session.formateur?.name} {session.formateur?.surname}</div>
                      <div className="text-[10px] text-zinc-400">Referent Technique</div>
                    </div>
                  </div>
                </TableCell>
                <TableCell className="text-center py-6">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-800 font-bold text-xs">
                     {session.nombre_inscrits} / {session.capacite_max}
                  </div>
                </TableCell>
                    <TableCell className="text-right">
                  <div className="flex justify-end gap-2">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="h-8 w-8 p-0 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800"
                      onClick={() => setEditingSession(session)}
                    >
                      <MoreVertical size={14} />
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="h-8 w-8 p-0 rounded-lg text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
                      onClick={async () => {
                        if(confirm("Supprimer cette session ?")) {
                          await deleteSession(session.id);
                          loadData();
                        }
                      }}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );

  const renderUsers = () => (
    <Card className="border-none glass-card animate-in fade-in duration-700">
      <CardHeader className="p-10 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-3xl font-black uppercase italic tracking-tighter">Annuaire Simplon</CardTitle>
          <CardDescription>Base de données des intervenants et étudiants ({data.totalUsers}).</CardDescription>
        </div>
        <div className="flex gap-2">
           <Button variant="outline" className="rounded-full">EXPORTER CSV</Button>
           <Button 
             className="bg-[#CE0033] text-white rounded-full"
             onClick={() => setIsUserModalOpen(true)}
           >
             NOUVEL UTILISATEUR
           </Button>
        </div>
      </CardHeader>
      
      {isUserModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-zinc-950 w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-zinc-900 animate-in zoom-in-95 duration-200">
            <h3 className="text-2xl font-black uppercase italic mb-6">Nouvel Utilisateur</h3>
            <form onSubmit={handleCreateUser} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Prénom</label>
                  <input 
                    required
                    value={newUser.name}
                    onChange={e => setNewUser({...newUser, name: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Nom (Surname)</label>
                  <input 
                    required
                    value={newUser.surname}
                    onChange={e => setNewUser({...newUser, surname: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
              </div>
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Email</label>
                <input 
                  type="email"
                  required
                  value={newUser.email}
                  onChange={e => setNewUser({...newUser, email: e.target.value})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Date de Naissance</label>
                  <input 
                    type="date"
                    required
                    value={newUser.birth_date}
                    onChange={e => setNewUser({...newUser, birth_date: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Rôle</label>
                  <select 
                    value={newUser.role}
                    onChange={e => setNewUser({...newUser, role: e.target.value as User['role']})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  >
                    <option value="Etudiant">Étudiant</option>
                    <option value="Formateur">Formateur</option>
                    <option value="Administrateur">Administrateur</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-4 mt-8">
                <Button variant="ghost" className="flex-1 rounded-xl" onClick={() => setIsUserModalOpen(false)}>ANNULER</Button>
                <Button type="submit" className="flex-1 bg-[#CE0033] text-white rounded-xl">CRÉER</Button>
              </div>
            </form>
          </div>
        </div>
      )}

      <CardContent className="p-0">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-1 px-1">
          {data.users.map((user) => (
            <div key={user.id} className="p-6 border border-zinc-50 dark:border-zinc-900 rounded-2xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-all flex items-center gap-6 group">
               <div className="size-14 rounded-2xl bg-gradient-to-tr from-zinc-900 to-zinc-700 dark:from-zinc-100 dark:to-zinc-300 flex items-center justify-center text-white dark:text-black font-black text-xl shadow-lg relative">
                  {user.name?.[0]}
                  {!user.is_active && (
                    <div className="absolute -top-1 -right-1 size-4 bg-red-500 rounded-full border-2 border-white dark:border-zinc-950"></div>
                  )}
               </div>
               <div className="flex-1">
                 <div className="font-bold text-zinc-900 dark:text-zinc-100 group-hover:text-[#CE0033] transition-colors uppercase italic">{user.name} {user.surname}</div>
                 <div className="text-xs text-zinc-400 font-medium mb-1">{user.email}</div>
                 <span className={`text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-md ${user.role === 'Formateur' ? 'bg-[#CE0033] text-white' : 'bg-black text-white'}`}>
                    {user.role}
                 </span>
               </div>
                 <div className="flex flex-col gap-2">
                   <Button 
                     variant="ghost" 
                     size="icon" 
                     className="rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                     onClick={() => setEditingUser(user)}
                   >
                     <MoreVertical size={16} />
                   </Button>
                   <Button 
                      variant="ghost" 
                      size="icon" 
                      className="rounded-full text-zinc-300 hover:text-red-500"
                      onClick={async () => {
                        if(confirm(`Supprimer l'utilisateur ${user.name} ?`)) {
                          await deleteUser(user.id);
                          loadData();
                        }
                      }}
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    </Button>
                   <ChevronRight size={18} className="text-zinc-300 group-hover:translate-x-1 transition-all" />
                 </div>
            </div>
          ))}
        </div>
      </CardContent>

      {editingUser && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-zinc-950 w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-zinc-900 animate-in zoom-in-95 duration-200">
            <h3 className="text-2xl font-black uppercase italic mb-6">Éditer Utilisateur</h3>
            <form onSubmit={handleUpdateUser} className="space-y-4">
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Email</label>
                <input 
                  type="email"
                  required
                  value={editingUser.email}
                  onChange={e => setEditingUser({...editingUser, email: e.target.value})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Prénom</label>
                  <input 
                    required
                    value={editingUser.name}
                    onChange={e => setEditingUser({...editingUser, name: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Nom</label>
                  <input 
                    required
                    value={editingUser.surname}
                    onChange={e => setEditingUser({...editingUser, surname: e.target.value})}
                    className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                  />
                </div>
              </div>
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Rôle</label>
                <select 
                  value={editingUser.role}
                  onChange={e => setEditingUser({...editingUser, role: e.target.value as User['role']})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                >
                  <option value="Etudiant">Étudiant</option>
                  <option value="Formateur">Formateur</option>
                  <option value="Administrateur">Administrateur</option>
                </select>
              </div>
              <div className="flex gap-4 mt-8">
                <Button variant="ghost" className="flex-1 rounded-xl" onClick={() => setEditingUser(null)}>ANNULER</Button>
                <Button type="submit" className="flex-1 bg-black text-white dark:bg-white dark:text-black rounded-xl">ENREGISTRER</Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </Card>
  );

  return (
    <div className="min-h-screen bg-white dark:bg-[#0A0A0A] selection:bg-[#CE0033] selection:text-white">
      {/* Sidebar - Desktop */}
      <aside className="fixed left-0 top-0 hidden h-screen w-72 border-r border-zinc-100 dark:border-zinc-900 bg-white/80 dark:bg-zinc-950/80 backdrop-blur-3xl p-8 lg:block z-50">
        <div className="flex items-center gap-4 mb-20 group cursor-pointer" onClick={() => setView('dashboard')}>
          <div className="relative">
            <div className="bg-white dark:bg-zinc-900 size-12 rounded-2xl flex items-center justify-center border border-zinc-100 dark:border-zinc-800 shadow-sm overflow-hidden group-hover:scale-105 transition-transform duration-500">
               <svg viewBox="0 0 100 100" className="size-8">
                  <circle cx="50" cy="50" r="40" stroke="#CE0033" strokeWidth="8" fill="none" />
                  <rect x="44" y="35" width="12" height="12" fill="#CE0033" />
                  <rect x="44" y="53" width="12" height="12" fill="#CE0033" />
               </svg>
            </div>
          </div>
          <div>
            <div className="font-black text-2xl tracking-tighter leading-none italic uppercase flex items-center gap-1">
              <span className="text-zinc-900 dark:text-white">Simplon</span>
              <span className="text-[#CE0033]">.</span>
            </div>
            <div className="text-[10px] font-bold text-zinc-400 tracking-widest uppercase">Admin System</div>
          </div>
        </div>

        <nav className="space-y-4">
          <SidebarLink icon={LayoutDashboard} label="Tableau de Bord" active={view === 'dashboard'} onClick={() => setView('dashboard')} />
          <SidebarLink icon={GraduationCap} label="Nos Formations" active={view === 'formations'} onClick={() => setView('formations')} />
          <SidebarLink icon={Calendar} label="Gestion Sessions" active={view === 'sessions'} onClick={() => setView('sessions')} />
          <SidebarLink icon={Users} label="Utilisateurs" active={view === 'utilisateurs'} onClick={() => setView('utilisateurs')} />
          <SidebarLink icon={BarChart3} label="Statistiques" active={view === 'stats'} onClick={() => setView('stats')} />
          <SidebarLink icon={Settings} label="Système" active={view === 'settings'} onClick={() => setView('settings')} />
        </nav>

        <div className="absolute bottom-8 left-8 right-8 p-6 rounded-3xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800">
           <div className="text-[10px] font-black uppercase text-zinc-400 mb-2">Build v2.6.0</div>
           <div className="flex items-center gap-3">
              <div className="size-8 rounded-full bg-green-500 animate-pulse ring-4 ring-green-500/10"></div>
              <div className="text-xs font-bold">API STATUS: ONLINE</div>
           </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-72 p-6 md:p-12 lg:p-16">
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-16">
          <div className="animate-in fade-in slide-in-from-left-4 duration-500">
            <div className="flex items-center gap-3 mb-2">
               <span className="bg-[#CE0033]/10 text-[#CE0033] text-[10px] font-black px-3 py-1 rounded-full uppercase tracking-widest">Simplon Admin Cloud</span>
               <span className="text-zinc-300">/</span>
               <span className="text-zinc-400 text-[10px] font-bold uppercase tracking-widest">{view}</span>
            </div>
            <h1 className="text-5xl font-black tracking-tighter text-zinc-900 dark:text-zinc-50 italic">
              Dashboard <span className="text-[#CE0033]">Centrale</span>
            </h1>
            <p className="text-zinc-500 mt-2 font-medium">Bon retour, Pilote <span className="text-zinc-900 dark:text-zinc-100 font-bold underline decoration-[#CE0033] underline-offset-4">Amaury</span>. Vos indicateurs sont au vert.</p>
          </div>
          <div className="flex items-center gap-4 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="relative group">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400 group-hover:text-[#CE0033] transition-all" size={20} />
              <input
                type="text"
                placeholder="RECHERCHER SUR LE RÉSEAU..."
                className="pl-12 pr-6 py-4 bg-zinc-50 dark:bg-zinc-900 border-none rounded-2xl text-[10px] font-black tracking-widest outline-none focus:ring-4 focus:ring-[#CE0033]/10 dark:focus:ring-white/5 transition-all w-full md:w-80 shadow-inner"
              />
            </div>
            <Button 
              className="rounded-2xl h-14 w-14 bg-black dark:bg-white text-white dark:text-black hover:scale-105 active:scale-95 transition-all flex items-center justify-center p-0 shadow-xl"
              onClick={() => {
                if (view === 'formations') setIsFormationModalOpen(true);
                else if (view === 'utilisateurs') setIsUserModalOpen(true);
                else if (view === 'sessions') setIsSessionModalOpen(true);
                else setView('formations'); // Default action
              }}
            >
              <Plus size={24} />
            </Button>
          </div>
        </header>

        {/* Dynamic Content */}
        {loading ? (
             <div className="h-[60vh] flex flex-col items-center justify-center animate-pulse">
                <div className="size-20 bg-[#CE0033] rounded-3xl mb-8 flex items-center justify-center">
                   <div className="size-10 bg-white/20 rounded-full animate-ping"></div>
                </div>
                <div className="text-[10px] font-black tracking-[0.3em] text-[#CE0033]">INITIALIZING SYSTEMS...</div>
             </div>
        ) : (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
            {view === 'dashboard' && renderDashboard()}
            {view === 'formations' && renderFormations()}
            {view === 'sessions' && renderSessions()}
            {view === 'utilisateurs' && renderUsers()}
            {view === 'stats' && (
              <div className="p-20 text-center border-4 border-dashed border-zinc-100 dark:border-zinc-900 rounded-[4rem]">
                <BarChart3 size={80} className="mx-auto text-zinc-200 mb-8" />
                <h2 className="text-3xl font-black italic uppercase">Statistiques Avancées</h2>
                <p className="text-zinc-500 max-w-sm mx-auto mt-4">Module d&apos;analyse de données en cours de déploiement sur votre instance.</p>
              </div>
            )}
            {view === 'settings' && (
              <div className="p-20 text-center border-4 border-dashed border-zinc-100 dark:border-zinc-900 rounded-[4rem]">
                <Settings size={80} className="mx-auto text-zinc-200 mb-8" />
                <h2 className="text-3xl font-black italic uppercase">Paramètres Réseau</h2>
                <p className="text-zinc-500 max-w-sm mx-auto mt-4">Configuration de la passerelle API et des protocoles de sécurité.</p>
              </div>
            )}
          </div>
        )}
        
        {error && (
          <div className="fixed bottom-8 right-8 max-w-md bg-red-50 border-l-4 border-red-500 p-6 rounded-2xl shadow-2xl animate-in slide-in-from-right-8 duration-500 z-[200]">
            <div className="flex items-start gap-4">
              <div className="size-10 bg-red-500 rounded-full flex items-center justify-center text-white shrink-0">
                <BarChart3 size={20} />
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-black uppercase text-red-900 mb-1">Erreur de Connexion API</h3>
                <p className="text-xs text-red-700 leading-relaxed mb-4">{error}</p>
                <Button 
                  size="sm" 
                  className="bg-red-900 text-white rounded-xl text-[10px] font-black uppercase tracking-widest px-4"
                  onClick={loadData}
                >
                  Réessayer la connexion
                </Button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Global Modals/Edit Modals would go here if not inside render functions */}
      {/* (they are currently inside render functions for context, which is fine as long as they aren't duplicated) */}
      {editingSession && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-zinc-950 w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-zinc-900 animate-in zoom-in-95 duration-200">
            <h3 className="text-2xl font-black uppercase italic mb-6">Modifier Session</h3>
            <form onSubmit={handleUpdateSession} className="space-y-4">
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Capacité Max</label>
                <input 
                  type="number"
                  required
                  value={editingSession.capacite_max}
                  onChange={e => setEditingSession({...editingSession, capacite_max: parseInt(e.target.value)})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                />
              </div>
              <div>
                <label className="text-[10px] font-black uppercase text-zinc-400 block mb-1">Statut</label>
                <select 
                  value={editingSession.statut}
                  onChange={e => setEditingSession({...editingSession, statut: e.target.value as Session['statut']})}
                  className="w-full bg-zinc-50 dark:bg-zinc-900 border-none rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20"
                >
                  <option value="planifiée">Planifiée</option>
                  <option value="en_cours">En Cours</option>
                  <option value="terminée">Terminée</option>
                  <option value="annulée">Annulée</option>
                </select>
              </div>
              <div className="flex gap-4 mt-8">
                <Button variant="ghost" className="flex-1 rounded-xl" onClick={() => setEditingSession(null)}>ANNULER</Button>
                <Button type="submit" className="flex-1 bg-black text-white dark:bg-white dark:text-black rounded-xl">ENREGISTRER</Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function SidebarLink({ icon: Icon, label, active = false, onClick }: SidebarLinkProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center justify-between px-6 py-4 rounded-3xl transition-all duration-300 group relative overflow-hidden
        ${active
          ? 'bg-[#CE0033] text-white shadow-[0_10px_30px_rgba(206,0,51,0.25)]'
          : 'text-zinc-500 hover:bg-zinc-50 dark:text-zinc-400 dark:hover:bg-zinc-900/50'}`}
    >
      <div className="flex items-center gap-4 relative z-10">
        <Icon size={22} className={`${active ? 'text-white' : 'text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-zinc-100'} transition-colors duration-300`} />
        <span className={`text-[11px] font-black uppercase tracking-widest ${active ? 'italic' : ''}`}>{label}</span>
      </div>
      {active && <div className="absolute top-0 right-0 h-full w-2 bg-white/20"></div>}
      {!active && <ChevronRight size={14} className="opacity-0 group-hover:opacity-100 transition-all translate-x-2 group-hover:translate-x-0" />}
    </button>
  );
}
