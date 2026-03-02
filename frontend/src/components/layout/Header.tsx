"use client";

import React from "react";
import { Search, Plus, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ViewType } from "@/lib/types";

const PAGE_META: Record<ViewType, { title: string; accent: string; sub: string }> = {
  dashboard:    { title: "Tableau de",    accent: "Bord",        sub: "Vos indicateurs sont au vert." },
  formations:   { title: "Catalogue",     accent: "Formations",  sub: "Parcours certifiants disponibles." },
  sessions:     { title: "Gestion des",   accent: "Sessions",    sub: "Planification pédagogique." },
  utilisateurs: { title: "Annuaire",      accent: "Simplon",     sub: "Intervenants & apprenants." },
  stats:        { title: "Analyse &",     accent: "Statistiques",sub: "Indicateurs de performance." },
  settings:     { title: "Paramètres",    accent: "Réseau",      sub: "Configuration du système." },
};

interface HeaderProps {
  view: ViewType;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  onAddClick: () => void;
  onMenuClick: () => void;
}

export function Header({ view, searchQuery, onSearchChange, onAddClick, onMenuClick }: HeaderProps) {
  const meta = PAGE_META[view];

  return (
    <header className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
      {/* Title block */}
      <div className="animate-in fade-in slide-in-from-left-4 duration-500 flex items-start gap-4">
        {/* Mobile hamburger */}
        <button
          className="lg:hidden mt-1 p-2 rounded-xl text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors"
          onClick={onMenuClick}
        >
          <Menu size={22} />
        </button>

        <div>
          {/* Breadcrumb */}
          <div className="flex items-center gap-2 mb-2">
            <span className="inline-flex items-center gap-1.5 bg-[#CE0033]/10 text-[#CE0033] label-xs px-3 py-1 rounded-full">
              <span className="size-1.5 bg-[#CE0033] rounded-full" />
              Simplon Admin
            </span>
            <span className="text-zinc-300 dark:text-zinc-700">/</span>
            <span className="label-xs text-zinc-400 dark:text-zinc-600">{view}</span>
          </div>

          {/* Page title */}
          <h1 className="heading-xxl text-zinc-900 dark:text-zinc-50">
            {meta.title}{" "}
            <span className="text-[#CE0033] dark:text-glow-red">{meta.accent}</span>
          </h1>
          <p className="text-sm text-zinc-500 dark:text-zinc-500 mt-1.5 font-medium">
            {meta.sub}
          </p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3 animate-in fade-in slide-in-from-right-4 duration-500">
        {/* Search */}
        <div className="relative group">
          <Search
            className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 group-hover:text-[#CE0033] transition-colors"
            size={15}
          />
          <input
            type="text"
            value={searchQuery}
            onChange={e => onSearchChange(e.target.value)}
            placeholder="Rechercher..."
            className="pl-10 pr-4 py-2.5 bg-zinc-100 dark:bg-white/[0.04] border border-transparent dark:border-white/[0.06] rounded-xl text-xs font-medium outline-none focus:ring-2 focus:ring-[#CE0033]/20 dark:focus:ring-[#CE0033]/15 transition-all w-52 dark:text-zinc-200 dark:placeholder:text-zinc-600"
          />
        </div>

        {/* Add button */}
        <Button
          onClick={onAddClick}
          className="rounded-xl h-10 w-10 bg-[#CE0033] hover:bg-[#b3002d] text-white flex items-center justify-center p-0 shadow-lg shadow-[rgba(206,0,51,0.3)] hover:shadow-[rgba(206,0,51,0.5)] transition-all active:scale-95"
        >
          <Plus size={18} />
        </Button>
      </div>
    </header>
  );
}
