"use client";

import React from "react";
import { BarChart3 } from "lucide-react";

export function StatsView() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center animate-in fade-in duration-500">
      <div className="size-24 rounded-3xl bg-[#CE0033]/10 dark:bg-[#CE0033]/5 flex items-center justify-center mb-6 relative">
        <BarChart3 size={44} className="text-[#CE0033]" />
        <div className="absolute inset-0 rounded-3xl border border-[#CE0033]/20 animate-pulse" />
      </div>
      <h2 className="heading-lg text-zinc-900 dark:text-zinc-50 mb-3">
        Statistiques <span className="text-[#CE0033]">Avancées</span>
      </h2>
      <p className="text-sm text-zinc-400 max-w-xs leading-relaxed">
        Module d&apos;analyse de données en cours de déploiement sur votre instance.
      </p>
      <div className="mt-8 flex items-center gap-2">
        <div className="size-2 rounded-full bg-amber-400 animate-pulse" />
        <span className="label-xs text-amber-400">DÉPLOIEMENT EN COURS</span>
      </div>
    </div>
  );
}
