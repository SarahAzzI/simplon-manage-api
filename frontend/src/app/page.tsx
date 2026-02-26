"use client";

import {
  Users,
  GraduationCap,
  Calendar,
  Settings,
  BarChart3,
  LayoutDashboard,
  Plus,
  ArrowUpRight,
  Search
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

interface SidebarLinkProps {
  icon: React.ElementType;
  label: string;
  active?: boolean;
}

export default function DashboardPage() {
  const stats = [
    { name: "Total Étudiants", value: "128", icon: Users, color: "text-blue-600", bg: "bg-blue-50" },
    { name: "Formations Actives", value: "12", icon: GraduationCap, color: "text-purple-600", bg: "bg-purple-50" },
    { name: "Sessions à venir", value: "5", icon: Calendar, color: "text-orange-600", bg: "bg-orange-50" },
    { name: "Taux de remplissage", value: "84%", icon: BarChart3, color: "text-green-600", bg: "bg-green-50" },
  ];

  const recentSessions = [
    { id: 1, formation: "Développeur Web", date: "15 Mars 2026", formateur: "Sarah AzzI", status: "Confirmé", fill: "18/20" },
    { id: 2, formation: "Data Analyst", date: "22 Mars 2026", formateur: "Marc Durand", status: "En attente", fill: "12/15" },
    { id: 3, formation: "DevOps Expert", date: "02 Avril 2026", formateur: "Julie Martin", status: "Confirmé", fill: "10/10" },
    { id: 4, formation: "Cybersécurité", date: "10 Avril 2026", formateur: "Thomas Petit", status: "Ouvert", fill: "5/12" },
  ];

  const calculateFillPercentage = (fillStr: string) => {
    const [current, total] = fillStr.split("/").map(Number);
    return (current / total) * 100;
  };

  return (
    <div className="min-h-screen bg-zinc-50/50 dark:bg-zinc-950">
      {/* Sidebar - Desktop */}
      <aside className="fixed left-0 top-0 hidden h-screen w-64 border-r bg-white p-6 dark:bg-zinc-900 lg:block">
        <div className="flex items-center gap-2 font-bold text-xl mb-10 text-blue-600">
          <div className="bg-blue-600 text-white p-1.5 rounded-lg">
            <GraduationCap size={24} />
          </div>
          Simplon Manage
        </div>

        <nav className="space-y-2">
          <SidebarLink icon={LayoutDashboard} label="Dashboard" active />
          <SidebarLink icon={GraduationCap} label="Formations" />
          <SidebarLink icon={Calendar} label="Sessions" />
          <SidebarLink icon={Users} label="Utilisateurs" />
          <SidebarLink icon={BarChart3} label="Statistiques" />
          <SidebarLink icon={Settings} label="Paramètres" />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 p-4 md:p-8 lg:p-10">
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">Bonjour, Amaury 👋</h1>
            <p className="text-zinc-500 dark:text-zinc-400">Voici un aperçu de l&apos;activité du centre de formation.</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="relative group">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400 group-hover:text-blue-500 transition-colors" size={18} />
              <input
                type="text"
                placeholder="Rechercher..."
                className="pl-10 pr-4 py-2 bg-white border rounded-full text-sm outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all w-full md:w-64 dark:bg-zinc-900"
              />
            </div>
            <Button className="rounded-full bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-500/20 transition-all active:scale-95">
              <Plus size={18} className="mr-1" /> Nouveau
            </Button>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          {stats.map((stat, i) => (
            <Card key={i} className="border-none shadow-sm hover:shadow-md transition-shadow group overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400 mb-1">{stat.name}</p>
                    <h3 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">{stat.value}</h3>
                  </div>
                  <div className={`${stat.bg} ${stat.color} p-3 rounded-2xl group-hover:scale-110 transition-transform`}>
                    <stat.icon size={24} />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-xs text-green-600 font-medium">
                  <ArrowUpRight size={14} className="mr-1" />
                  <span>+12% ce mois-ci</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Content Tabs/Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Main Table */}
          <Card className="xl:col-span-2 border-none shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between p-6 pb-2">
              <div>
                <CardTitle className="text-xl">Prochaines Sessions</CardTitle>
                <CardDescription>Les sessions de formation prévues ce mois-ci.</CardDescription>
              </div>
              <Button variant="ghost" className="text-blue-600 hover:text-blue-700 hover:bg-blue-50">Voir tout</Button>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow className="hover:bg-transparent border-zinc-100">
                    <TableHead className="pl-6 font-semibold">Formation</TableHead>
                    <TableHead className="font-semibold text-center">Date</TableHead>
                    <TableHead className="font-semibold text-center">Remplissage</TableHead>
                    <TableHead className="font-semibold text-center">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentSessions.map((session) => (
                    <TableRow key={session.id} className="group border-zinc-50 hover:bg-zinc-50/50 transition-colors">
                      <TableCell className="pl-6 py-4">
                        <div className="font-medium text-zinc-900">{session.formation}</div>
                        <div className="text-xs text-zinc-500">{session.formateur}</div>
                      </TableCell>
                      <TableCell className="text-center text-sm text-zinc-600">{session.date}</TableCell>
                      <TableCell className="text-center">
                        <div className="flex flex-col items-center gap-1.5">
                          <span className="text-xs font-medium">{session.fill}</span>
                          <div className="w-24 h-1.5 bg-zinc-100 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-blue-500 rounded-full"
                              style={{ width: `${calculateFillPercentage(session.fill)}%` }}
                            ></div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell className="text-center pr-6">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-medium 
                          ${session.status === 'Confirmé' ? 'bg-green-100 text-green-700' :
                            session.status === 'Ouvert' ? 'bg-blue-100 text-blue-700' :
                              'bg-orange-100 text-orange-700'}`}>
                          {session.status}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          {/* Stats Chart & Quick Actions */}
          <div className="space-y-6">
            <Card className="border-none shadow-sm">
              <CardHeader>
                <CardTitle className="text-lg">Inscriptions Mensuelles</CardTitle>
                <CardDescription>Évolution des inscriptions sur 6 mois.</CardDescription>
              </CardHeader>
              <CardContent className="pb-6">
                <StatsChart />
              </CardContent>
            </Card>

            <Card className="border-none shadow-sm bg-blue-600 text-white overflow-hidden relative">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <GraduationCap size={120} />
              </div>
              <CardHeader>
                <CardTitle>Nouveau Badge</CardTitle>
                <CardDescription className="text-blue-100">Plus de 50 inscriptions cette semaine !</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm mb-4 text-blue-50">Bravo Amaury, la formation &quot;Développeur Web&quot; est un grand succès cette année.</p>
                <Button variant="secondary" className="w-full rounded-full font-semibold text-blue-600">Gérer les dossiers</Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}

function SidebarLink({ icon: Icon, label, active = false }: SidebarLinkProps) {
  return (
    <a
      href="#"
      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group
        ${active
          ? 'bg-blue-50 text-blue-600 font-semibold'
          : 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800'}`}
    >
      <Icon size={20} className={`${active ? 'text-blue-600' : 'text-zinc-400 group-hover:text-zinc-700'} transition-colors`} />
      {label}
    </a>
  );
}
