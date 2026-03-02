"use client";

import React from "react";
import { Settings } from "lucide-react";

export function SettingsView() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center animate-in fade-in duration-500">
      <div className="size-24 rounded-3xl bg-zinc-100 dark:bg-white/[0.04] flex items-center justify-center mb-6 relative">
        <Settings size={44} className="text-zinc-400 dark:text-zinc-600 animate-[spin_10s_linear_infinite]" />
        <div className="absolute inset-0 rounded-3xl border border-zinc-200 dark:border-white/[0.08]" />
      </div>
      <h2 className="heading-lg text-zinc-900 dark:text-zinc-50 mb-3">
        Paramètres <span className="text-[#CE0033]">Réseau</span>
      </h2>
      <p className="text-sm text-zinc-400 max-w-xs leading-relaxed">
        Configuration de la passerelle API et des protocoles de sécurité.
      </p>
      <div className="mt-8 flex items-center gap-2">
        <div className="size-2 rounded-full bg-zinc-400" />
        <span className="label-xs text-zinc-400">BIENTÔT DISPONIBLE</span>
      </div>
    </div>
  );
}
