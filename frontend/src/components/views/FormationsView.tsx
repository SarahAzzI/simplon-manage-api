"use client";

import React from "react";
import { GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Formation } from "@/lib/api";

interface FormationsViewProps {
  formations: Formation[];
  searchQuery: string;
  onAdd: () => void;
  onEdit: (f: Formation) => void;
  onDelete: (f: Formation) => void;
}

const LEVEL_COLORS: Record<string, string> = {
  "débutant": "bg-emerald-500/10 text-emerald-500",
  "intermédiaire": "bg-sky-500/10 text-sky-500",
  "avancé": "bg-violet-500/10 text-violet-500",
  "Bac+2": "bg-amber-500/10 text-amber-500",
  "Bac+3": "bg-sky-500/10 text-sky-500",
  "Bac+5": "bg-violet-500/10 text-violet-500",
};

export function FormationsView({
  formations, searchQuery, onEdit, onDelete,
}: FormationsViewProps) {
  const filtered = formations.filter(f =>
    f.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    f.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (filtered.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-center">
        <div className="size-20 rounded-3xl bg-zinc-100 dark:bg-white/5 flex items-center justify-center mb-6">
          <GraduationCap size={40} className="text-zinc-300 dark:text-zinc-700" />
        </div>
        <h3 className="heading-md text-zinc-900 dark:text-zinc-100 mb-2">
          {searchQuery ? "Aucun résultat" : "Aucune formation"}
        </h3>
        <p className="text-sm text-zinc-400">
          {searchQuery ? `Pas de formation trouvée pour "${searchQuery}"` : "Cliquez sur + pour ajouter votre première formation."}
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 animate-in fade-in duration-500">
      {filtered.map((formation) => {
        const levelColor = LEVEL_COLORS[formation.level] ?? "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400";
        return (
          <Card
            key={formation.id}
            className="border-none glass-card hover:shadow-2xl hover:-translate-y-1.5 transition-all duration-500 group overflow-hidden"
          >
            {/* Card header with gradient */}
            <div className="h-28 bg-gradient-to-br from-[#CE0033] via-[#b3002d] to-zinc-900 p-5 relative overflow-hidden">
              <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0wIDBoMjB2MjBIMHoiLz48cGF0aCBkPSJNMSAxaDFNMSA1aDFNMSA5aDFNMSAxM2gxTTEgMTdoMU01IDFoMU01IDVoMU01IDloMU01IDEzaDFNNSAxN2gxTTkgMWgxTTkgNWgxTTkgOWgxTTkgMTNoMU05IDE3aDFNMTMgMWgxTTEzIDVoMU0xMyA5aDFNMTMgMTNoMU0xMyAxN2gxTTE3IDFoMU0xNyA1aDFNMTcgOWgxTTE3IDEzaDFNMTcgMTdoMSIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjA2KSIvPjwvZz48L3N2Zz4=')] opacity-50" />
              <GraduationCap
                className="absolute top-3 right-3 text-white/15 group-hover:text-white/25 group-hover:rotate-6 transition-all duration-500"
                size={52}
              />
              <div className="absolute bottom-4 left-5 text-white font-black text-lg uppercase italic leading-tight group-hover:scale-105 transition-transform origin-left duration-300 pr-14">
                {formation.title}
              </div>
            </div>

            <CardContent className="p-5">
              {/* Badges */}
              <div className="flex items-center gap-2 mb-3.5">
                <span className={`label-xs px-2.5 py-1 rounded-full ${levelColor}`}>
                  {formation.level || "Expert"}
                </span>
                <span className="label-xs text-zinc-400 dark:text-zinc-600">
                  {formation.duration || 0} MOIS
                </span>
              </div>

              {/* Description */}
              <p className="text-sm text-zinc-500 dark:text-zinc-500 leading-relaxed mb-5 line-clamp-2">
                {formation.description || "Aucune description disponible."}
              </p>

              {/* Actions */}
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  className="flex-1 rounded-xl border border-zinc-100 dark:border-white/[0.06] hover:bg-zinc-50 dark:hover:bg-white/[0.04] label-xs transition-all"
                  onClick={() => onEdit(formation)}
                >
                  Éditer
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="flex-1 rounded-xl border border-zinc-100 dark:border-white/[0.06] hover:bg-red-50 dark:hover:bg-[#CE0033]/10 label-xs text-red-500 hover:text-[#CE0033] transition-all"
                  onClick={() => onDelete(formation)}
                >
                  Supprimer
                </Button>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
