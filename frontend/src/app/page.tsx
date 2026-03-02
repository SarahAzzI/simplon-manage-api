"use client";

import React, { useState, useEffect, useMemo } from "react";
import { SidebarContent } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Sheet } from "@/components/ui/sheet";
import { AlertDialog } from "@/components/ui/alert-dialog";
import { useToast } from "@/components/ui/toast";

// Views
import { DashboardView } from "@/components/views/DashboardView";
import { FormationsView } from "@/components/views/FormationsView";
import { SessionsView } from "@/components/views/SessionsView";
import { UsersView } from "@/components/views/UsersView";
import { StatsView } from "@/components/views/StatsView";
import { SettingsView } from "@/components/views/SettingsView";

// Modals
import { FormationModal } from "@/components/modals/FormationModal";
import { SessionModal } from "@/components/modals/SessionModal";
import { UserModal } from "@/components/modals/UserModal";

import { ViewType } from "@/lib/types";
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
  Session,
} from "@/lib/api";

export default function DashboardPage() {
  const { toast } = useToast();
  const [view, setView] = useState<ViewType>("dashboard");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [data, setData] = useState({
    users: [] as User[],
    formations: [] as Formation[],
    sessions: [] as Session[],
    totalUsers: 0,
    totalFormations: 0,
    totalSessions: 0,
  });

  // --- Modal States ---
  const [modalType, setModalType] = useState<"formation" | "session" | "user" | null>(null);
  const [modalMode, setModalMode] = useState<"create" | "edit">("create");
  const [activeItem, setActiveItem] = useState<any>(null);

  // --- Confirm Dialog State ---
  const [confirmConfig, setConfirmConfig] = useState<{
    open: boolean;
    title: string;
    description: string;
    onConfirm: () => void;
  }>({
    open: false,
    title: "",
    description: "",
    onConfirm: () => {},
  });

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
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
      toast({
        title: "Erreur de connexion",
        description: "Impossible de joindre l'API. Vérifiez que le backend est lancé.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const chartData = useMemo(() => {
    const months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"];
    const currentYear = new Date().getFullYear();
    const monthlyData = months.map((m) => ({ name: m, total: 0 }));

    data.sessions.forEach((s) => {
      const date = new Date(s.date_debut);
      if (date.getFullYear() === currentYear) {
        monthlyData[date.getMonth()].total += 1;
      }
    });

    return monthlyData.slice(0, 7);
  }, [data.sessions]);

  // --- Action Handlers ---

  const handleDelete = (type: "formation" | "session" | "user", item: any) => {
    const label = type === "user" ? `${item.name} ${item.surname}` : (item.title || "cette session");
    setConfirmConfig({
      open: true,
      title: "Confirmation de suppression",
      description: `Êtes-vous sûr de vouloir supprimer ${label} ? Cette action est irréversible.`,
      onConfirm: async () => {
        try {
          if (type === "formation") await deleteFormation(item.id);
          else if (type === "session") await deleteSession(item.id);
          else if (type === "user") await deleteUser(item.id);
          
          toast({ title: "Succès", description: "Élément supprimé avec succès.", variant: "success" });
          loadData();
        } catch (err: any) {
          toast({ title: "Erreur", description: err.message || "Erreur lors de la suppression.", variant: "destructive" });
        }
      },
    });
  };

  const handleOpenModal = (type: "formation" | "session" | "user", mode: "create" | "edit", item: any = null) => {
    setModalType(type);
    setModalMode(mode);
    
    if (mode === "edit") {
      setActiveItem({ ...item });
    } else {
      if (type === "formation") {
        setActiveItem({ title: "", description: "", duration: 6, level: "Bac+2" });
      } else if (type === "session") {
        setActiveItem({
          formation_id: 0,
          formateur_id: 0,
          date_debut: new Date().toISOString().split("T")[0],
          date_fin: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
          capacite_max: 20,
        });
      } else if (type === "user") {
        setActiveItem({ email: "", name: "", surname: "", birth_date: "2000-01-01", role: "Etudiant" });
      }
    }
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (modalType === "formation") {
        if (modalMode === "create") await createFormation(activeItem);
        else await updateFormation(activeItem.id, activeItem);
      } else if (modalType === "session") {
        if (modalMode === "create") await createSession(activeItem);
        else await updateSession(activeItem.id, activeItem);
      } else if (modalType === "user") {
        if (modalMode === "create") await createUser(activeItem);
        else await updateUser(activeItem.id, activeItem);
      }
      
      toast({
        title: "Opération réussie",
        description: modalMode === "create" ? "Création effectuée." : "Mise à jour effectuée.",
        variant: "success",
      });
      setModalType(null);
      loadData();
    } catch (err: any) {
      toast({ title: "Erreur", description: err.message || "Erreur lors de l'opération.", variant: "destructive" });
    }
  };

  const renderView = () => {
    switch (view) {
      case "dashboard":
        return (
          <DashboardView
            {...data}
            loading={loading}
            chartData={chartData}
            setView={setView}
          />
        );
      case "formations":
        return (
          <FormationsView
            formations={data.formations}
            searchQuery={searchQuery}
            onAdd={() => handleOpenModal("formation", "create")}
            onEdit={(f) => handleOpenModal("formation", "edit", f)}
            onDelete={(f) => handleDelete("formation", f)}
          />
        );
      case "sessions":
        return (
          <SessionsView
            sessions={data.sessions}
            searchQuery={searchQuery}
            onEdit={(s) => handleOpenModal("session", "edit", s)}
            onDelete={(s) => handleDelete("session", s)}
          />
        );
      case "utilisateurs":
        return (
          <UsersView
            users={data.users}
            totalUsers={data.totalUsers}
            searchQuery={searchQuery}
            onEdit={(u) => handleOpenModal("user", "edit", u)}
            onDelete={(u) => handleDelete("user", u)}
          />
        );
      case "stats":
        return <StatsView />;
      case "settings":
        return <SettingsView />;
      default:
        return <DashboardView {...data} loading={loading} chartData={chartData} setView={setView} />;
    }
  };

  return (
    <div className="min-h-screen bg-background selection:bg-[#CE0033] selection:text-white grid-bg transition-colors duration-500">
      <div className="scanlines" />

      {/* Sidebar - Desktop */}
      <aside className="fixed left-0 top-0 hidden h-screen w-72 sidebar-futuriste lg:block z-50">
        <SidebarContent view={view} setView={setView} apiOnline={!error} />
      </aside>

      {/* Sidebar - Mobile */}
      <Sheet open={isSidebarOpen} onOpenChange={setIsSidebarOpen}>
        <SidebarContent view={view} setView={(v) => { setView(v); setIsSidebarOpen(false); }} apiOnline={!error} />
      </Sheet>

      {/* Main Content */}
      <main className="lg:ml-72 p-6 md:p-10 lg:p-14 relative z-10 max-w-[1600px]">
        <Header
          view={view}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          onAddClick={() => {
            if (view === "formations") handleOpenModal("formation", "create");
            else if (view === "utilisateurs") handleOpenModal("user", "create");
            else if (view === "sessions") handleOpenModal("session", "create");
            else setView("formations");
          }}
          onMenuClick={() => setIsSidebarOpen(true)}
        />

        <div className="animate-in fade-in duration-700">
          {loading && view === "dashboard" && data.totalUsers === 0 ? (
            <div className="h-[60vh] flex flex-col items-center justify-center">
              <div className="size-16 bg-[#CE0033] rounded-2xl flex items-center justify-center animate-pulse glow-red">
                <div className="size-8 bg-white/20 rounded-full animate-ping" />
              </div>
              <div className="mt-6 label-xs text-[#CE0033] animate-pulse">Initialisation du système...</div>
            </div>
          ) : (
            renderView()
          )}
        </div>
      </main>

      {/* Modals */}
      {modalType === "formation" && (
        <FormationModal
          mode={modalMode}
          data={activeItem}
          onChange={setActiveItem}
          onClose={() => setModalType(null)}
          onSubmit={handleFormSubmit}
        />
      )}
      {modalType === "session" && (
        <SessionModal
          mode={modalMode}
          data={activeItem}
          formations={data.formations}
          formateurs={data.users.filter(u => u.role === "Formateur")}
          onChange={setActiveItem}
          onClose={() => setModalType(null)}
          onSubmit={handleFormSubmit}
        />
      )}
      {modalType === "user" && (
        <UserModal
          mode={modalMode}
          data={activeItem}
          onChange={setActiveItem}
          onClose={() => setModalType(null)}
          onSubmit={handleFormSubmit}
        />
      )}

      {/* Confirm Dialog */}
      <AlertDialog
        open={confirmConfig.open}
        onOpenChange={(open) => setConfirmConfig({ ...confirmConfig, open })}
        title={confirmConfig.title}
        description={confirmConfig.description}
        onConfirm={confirmConfig.onConfirm}
      />
    </div>
  );
}
