"use client";

import React from "react";
import { Calendar, MoreVertical } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Session } from "@/lib/api";

const STATUS_STYLE: Record<string, string> = {
  planifiée: "bg-sky-500/10 text-sky-500 dark:bg-sky-500/15 dark:text-sky-400",
  en_cours: "bg-emerald-500/10 text-emerald-500 dark:bg-emerald-500/15 dark:text-emerald-400",
  terminée: "bg-zinc-200/60 text-zinc-500 dark:bg-white/5 dark:text-zinc-500",
  annulée: "bg-[#CE0033]/10 text-[#CE0033]",
};
const STATUS_LABEL: Record<string, string> = {
  planifiée: "Planifiée",
  en_cours: "En cours",
  terminée: "Terminée",
  annulée: "Annulée",
};

interface SessionsViewProps {
  sessions: Session[];
  searchQuery: string;
  onEdit: (s: Session) => void;
  onDelete: (s: Session) => void;
}

export function SessionsView({ sessions, searchQuery, onEdit, onDelete }: SessionsViewProps) {
  const filtered = sessions.filter(s => {
    const q = searchQuery.toLowerCase();
    return (
      s.formation?.title?.toLowerCase().includes(q) ||
      s.formateur?.name?.toLowerCase().includes(q) ||
      s.formateur?.surname?.toLowerCase().includes(q)
    );
  });

  const getSessionStatus = (s: Session): string => {
    if (s.statut) return s.statut;
    const now = new Date();
    const debut = new Date(s.date_debut);
    const fin = new Date(s.date_fin);
    if (now < debut) return "planifiée";
    if (now > fin) return "terminée";
    return "en_cours";
  };

  return (
    <Card className="border-none glass-card overflow-hidden animate-in fade-in duration-500">
      <CardHeader className="p-7 pb-5 flex flex-row items-center justify-between bg-zinc-50/30 dark:bg-white/[0.01] border-b border-zinc-100 dark:border-white/[0.04]">
        <div>
          <CardTitle className="heading-lg">Planification Sessions</CardTitle>
          <CardDescription className="text-zinc-500 dark:text-zinc-600 mt-1">
            {filtered.length} session{filtered.length > 1 ? "s" : ""} affichée{filtered.length > 1 ? "s" : ""}
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="p-0">
        {filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="size-16 rounded-2xl bg-zinc-100 dark:bg-white/5 flex items-center justify-center mb-4">
              <Calendar size={32} className="text-zinc-300 dark:text-zinc-700" />
            </div>
            <p className="text-sm text-zinc-400">
              {searchQuery ? `Aucune session pour "${searchQuery}"` : "Aucune session disponible."}
            </p>
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="border-zinc-100 dark:border-white/[0.04] hover:bg-transparent">
                <TableHead className="pl-7 label-xs text-zinc-400">Période</TableHead>
                <TableHead className="label-xs text-zinc-400">Formation</TableHead>
                <TableHead className="label-xs text-zinc-400">Formateur</TableHead>
                <TableHead className="label-xs text-zinc-400 text-center">Occupation</TableHead>
                <TableHead className="label-xs text-zinc-400 text-center">Statut</TableHead>
                <TableHead className="pr-7" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((session) => {
                const status = getSessionStatus(session);
                const fillPct = session.capacite_max > 0
                  ? (session.nombre_inscrits / session.capacite_max) * 100
                  : 0;
                return (
                  <TableRow
                    key={session.id}
                    className="border-zinc-50 dark:border-white/[0.03] hover:bg-zinc-50/50 dark:hover:bg-white/[0.02] group transition-all"
                  >
                    <TableCell className="pl-7 py-5">
                      <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
                        {new Date(session.date_debut).toLocaleDateString("fr-FR")}
                      </div>
                      <div className="label-xs text-zinc-400 mt-0.5">
                        → {new Date(session.date_fin).toLocaleDateString("fr-FR")}
                      </div>
                    </TableCell>
                    <TableCell className="py-5">
                      <div className="font-bold text-sm italic text-zinc-700 dark:text-zinc-300 group-hover:text-[#CE0033] transition-colors uppercase">
                        {session.formation?.title || "MODULE EXTERNE"}
                      </div>
                    </TableCell>
                    <TableCell className="py-5">
                      <div className="flex items-center gap-2.5">
                        <div className="size-7 rounded-full bg-[#CE0033] flex items-center justify-center text-white text-[10px] font-bold shrink-0">
                          {session.formateur?.name?.[0]}{session.formateur?.surname?.[0]}
                        </div>
                        <div>
                          <div className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
                            {session.formateur?.name} {session.formateur?.surname}
                          </div>
                          <div className="label-xs text-zinc-400">Formateur</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-center py-5">
                      <div className="flex flex-col items-center gap-1.5">
                        <span className="text-xs font-bold text-zinc-900 dark:text-zinc-100">
                          {session.nombre_inscrits}/{session.capacite_max}
                        </span>
                        <div className="w-20 h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                          <div
                            className="h-full progress-bar-fill rounded-full"
                            style={{ width: `${fillPct}%` }}
                          />
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-center py-5">
                      <span className={`inline-block px-2.5 py-1 rounded-full label-xs ${STATUS_STYLE[status] ?? "bg-zinc-100 text-zinc-500"}`}>
                        {STATUS_LABEL[status] ?? status}
                      </span>
                    </TableCell>
                    <TableCell className="pr-7 py-5">
                      <div className="flex justify-end gap-1.5">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-8 w-8 p-0 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/[0.06]"
                          onClick={() => onEdit(session)}
                        >
                          <MoreVertical size={14} />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-8 w-8 p-0 rounded-lg text-red-400 hover:bg-red-50 dark:hover:bg-[#CE0033]/10 hover:text-[#CE0033]"
                          onClick={() => onDelete(session)}
                        >
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                          </svg>
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
