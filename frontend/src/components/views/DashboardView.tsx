"use client";

import React from "react";
import {
  Users, BookOpen, Calendar, BarChart3,
  ArrowUpRight, UserCheck, GraduationCap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { StatsChart } from "@/components/stats-chart";
import { User, Formation, Session } from "@/lib/api";
import { ViewType } from "@/lib/types";

interface DashboardViewProps {
  users: User[];
  formations: Formation[];
  sessions: Session[];
  totalUsers: number;
  totalFormations: number;
  totalSessions: number;
  loading: boolean;
  chartData: { name: string; total: number }[];
  setView: (v: ViewType) => void;
}

export function DashboardView({
  users, formations, sessions,
  loading, chartData, setView,
}: DashboardViewProps) {
  const totalStudents = users.filter(u => u.role === "Etudiant").length;
  const activeFormations = formations.length;
  const upcomingSessions = sessions.filter(s => new Date(s.date_debut) > new Date()).length;
  const totalCapacity = sessions.reduce((acc, s) => acc + s.capacite_max, 0);
  const totalInscriptions = sessions.reduce((acc, s) => acc + s.nombre_inscrits, 0);
  const fillRate = totalCapacity > 0 ? Math.round((totalInscriptions / totalCapacity) * 100) : 0;

  const stats = [
    {
      name: "Total Apprenants",
      value: totalStudents,
      icon: Users,
      color: "text-[#CE0033]",
      bg: "bg-[#CE0033]/10",
      trend: totalStudents > 0,
      trendLabel: totalStudents > 0 ? "Actifs" : "Aucun",
    },
    {
      name: "Formations actives",
      value: activeFormations,
      icon: BookOpen,
      color: "text-violet-400",
      bg: "bg-violet-500/10",
      trend: activeFormations > 0,
      trendLabel: activeFormations > 0 ? "En ligne" : "À créer",
    },
    {
      name: "Sessions à venir",
      value: upcomingSessions,
      icon: Calendar,
      color: "text-sky-400",
      bg: "bg-sky-500/10",
      trend: upcomingSessions > 0,
      trendLabel: upcomingSessions > 0 ? "Planifiées" : "Aucune",
    },
    {
      name: "Taux de remplissage",
      value: `${fillRate}%`,
      icon: BarChart3,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10",
      trend: fillRate > 50,
      trendLabel: `${fillRate}% rempli`,
    },
  ];

  const calcFill = (current: number, total: number) =>
    total > 0 ? (current / total) * 100 : 0;

  return (
    <>
      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
        {stats.map((stat, i) => (
          <Card
            key={i}
            className="border-none shadow-sm glass-card hover:-translate-y-1.5 hover:shadow-xl transition-all duration-300 group overflow-hidden relative stat-card-accent"
          >
            <CardContent className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="label-xs text-zinc-500 dark:text-zinc-600 mb-2">{stat.name}</p>
                  <h3 className="text-3xl font-black tracking-tighter text-zinc-900 dark:text-zinc-50">
                    {loading ? (
                      <span className="inline-block w-12 h-8 bg-zinc-200 dark:bg-zinc-800 rounded-lg animate-pulse" />
                    ) : stat.value}
                  </h3>
                </div>
                <div className={`${stat.bg} ${stat.color} p-3.5 rounded-2xl group-hover:scale-110 transition-transform duration-500 shrink-0`}>
                  <stat.icon size={22} />
                </div>
              </div>
              <div className={`mt-4 flex items-center gap-1 text-xs font-bold ${stat.trend ? "text-emerald-500" : "text-zinc-400"}`}>
                <ArrowUpRight size={13} className={stat.trend ? "" : "opacity-40"} />
                <span>{stat.trendLabel}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Sessions table */}
        <Card className="xl:col-span-2 border-none glass-card overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between p-7 pb-4">
            <div>
              <CardTitle className="text-xl font-black tracking-tight">Prochaines Sessions</CardTitle>
              <CardDescription className="text-zinc-500 dark:text-zinc-600 mt-0.5">
                Aperçu des formations imminentes.
              </CardDescription>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="rounded-full border-[#CE0033]/40 text-[#CE0033] hover:bg-[#CE0033] hover:text-white transition-colors text-xs font-bold"
              onClick={() => setView("sessions")}
            >
              Voir tout
            </Button>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent border-zinc-100/50 dark:border-zinc-900">
                  <TableHead className="pl-7 label-xs text-zinc-400">Formation</TableHead>
                  <TableHead className="label-xs text-zinc-400 text-center">Début</TableHead>
                  <TableHead className="label-xs text-zinc-400 text-center">Capacité</TableHead>
                  <TableHead className="label-xs text-zinc-400 text-center">Statut</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-12">
                      <div className="flex flex-col items-center gap-3">
                        <div className="size-8 rounded-xl bg-[#CE0033] animate-pulse" />
                        <span className="label-xs text-zinc-400 animate-pulse">Chargement...</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ) : sessions.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-12 text-zinc-400 text-sm">
                      Aucune session active actuellement.
                    </TableCell>
                  </TableRow>
                ) : sessions.slice(0, 5).map((session) => {
                  const isUpcoming = new Date(session.date_debut) > new Date();
                  return (
                    <TableRow
                      key={session.id}
                      className="group border-zinc-50/50 dark:border-zinc-900/50 hover:bg-zinc-50/80 dark:hover:bg-white/[0.02] transition-all cursor-pointer"
                    >
                      <TableCell className="pl-7 py-4">
                        <div className="font-bold text-zinc-900 dark:text-zinc-100 group-hover:text-[#CE0033] transition-colors text-sm">
                          {session.formation?.title || "Session Spéciale"}
                        </div>
                        <div className="flex items-center gap-1.5 mt-0.5">
                          <UserCheck size={11} className="text-[#CE0033]" />
                          <span className="text-xs text-zinc-400 font-medium">
                            {session.formateur?.name} {session.formateur?.surname}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="text-center text-sm font-medium text-zinc-600 dark:text-zinc-400">
                        {new Date(session.date_debut).toLocaleDateString("fr-FR", { day: "numeric", month: "short" })}
                      </TableCell>
                      <TableCell className="text-center">
                        <div className="flex flex-col items-center gap-1.5">
                          <span className="text-xs font-bold text-zinc-900 dark:text-zinc-100">
                            {session.nombre_inscrits}/{session.capacite_max}
                          </span>
                          <div className="w-20 h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                            <div
                              className="h-full progress-bar-fill rounded-full transition-all duration-1000"
                              style={{ width: `${calcFill(session.nombre_inscrits, session.capacite_max)}%` }}
                            />
                          </div>
                        </div>
                      </TableCell>
                      <TableCell className="text-center">
                        <span className={`inline-block px-2.5 py-1 rounded-full label-xs
                          ${isUpcoming
                            ? "bg-sky-500/10 text-sky-500 dark:bg-sky-500/15 dark:text-sky-400"
                            : "bg-[#CE0033]/10 text-[#CE0033]"
                          }`}>
                          {isUpcoming ? "À venir" : "En cours"}
                        </span>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Right column */}
        <div className="flex flex-col gap-5">
          {/* Chart */}
          <Card className="border-none glass-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg font-bold">Activité Sessions</CardTitle>
              <CardDescription className="text-zinc-500 dark:text-zinc-600">Inscriptions sur l&apos;année.</CardDescription>
            </CardHeader>
            <CardContent className="pb-6">
              <StatsChart data={chartData} />
            </CardContent>
          </Card>

          {/* Simplon Network CTA */}
          <Card className="border-none overflow-hidden relative group bg-gradient-to-br from-[#CE0033] via-[#d60036] to-[#1a0010]">
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBkPSJNMCAwaDFINDB2MUgweiIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjA1KSIvPjxwYXRoIGQ9Ik0wIDBoMXY0MEgweiIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjA1KSIvPjwvZz48L3N2Zz4=')] opacity-20" />
            <div className="absolute -top-8 -right-8 opacity-[0.08] group-hover:opacity-[0.12] transition-opacity duration-700">
              <GraduationCap size={180} className="text-white" />
            </div>
            <CardHeader className="relative z-10 pb-2">
              <CardTitle className="text-2xl font-black italic tracking-tighter uppercase text-white">
                Simplon Network
              </CardTitle>
              <CardDescription className="text-red-200/80 font-medium">
                Connecté au Cloud Simplon.
              </CardDescription>
            </CardHeader>
            <CardContent className="relative z-10">
              <p className="text-sm mb-5 text-red-100/70 leading-relaxed">
                Gérez vos formations et administrez vos sessions avec précision.
              </p>
              <Button
                variant="secondary"
                className="w-full rounded-xl font-black py-5 bg-white/10 hover:bg-white/20 text-white border border-white/20 shadow-none backdrop-blur-sm transition-all active:scale-95"
                onClick={() => setView("utilisateurs")}
              >
                ACCÈS ADMINISTRATEURS
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}
