"use client";

import React from "react";
import {
  LayoutDashboard,
  GraduationCap,
  Calendar,
  Users,
  BarChart3,
  Settings,
  ChevronRight,
} from "lucide-react";
import { ViewType } from "@/lib/types";

interface SidebarLinkProps {
  icon: React.ElementType;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

function SidebarLink({ icon: Icon, label, active = false, onClick }: SidebarLinkProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center justify-between px-5 py-3.5 rounded-2xl transition-all duration-300 group relative overflow-hidden
        ${active
          ? "bg-[#CE0033] text-white shadow-[0_8px_25px_rgba(206,0,51,0.35)] glow-red-sm"
          : "text-zinc-500 dark:text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 hover:bg-zinc-100 dark:hover:bg-white/5"
        }`}
    >
      {active && (
        <div className="absolute inset-0 bg-gradient-to-r from-[#CE0033] to-[#e6003a] opacity-100" />
      )}
      <div className="flex items-center gap-3.5 relative z-10">
        <Icon
          size={18}
          className={`${active ? "text-white" : "text-zinc-400 dark:text-zinc-600 group-hover:text-[#CE0033]"} transition-colors duration-300`}
        />
        <span className={`text-[11px] font-black uppercase tracking-widest ${active ? "text-white" : ""}`}>
          {label}
        </span>
      </div>
      <div className="relative z-10">
        {active ? (
          <div className="size-1.5 rounded-full bg-white/60" />
        ) : (
          <ChevronRight
            size={12}
            className="opacity-0 group-hover:opacity-40 transition-all -translate-x-1 group-hover:translate-x-0"
          />
        )}
      </div>
    </button>
  );
}

interface SidebarContentProps {
  view: ViewType;
  setView: (v: ViewType) => void;
  apiOnline: boolean;
}

export function SidebarContent({ view, setView, apiOnline }: SidebarContentProps) {
  return (
    <div className="flex flex-col h-full p-6 pt-8">
      {/* Logo */}
      <div
        className="flex items-center gap-3.5 mb-10 cursor-pointer group"
        onClick={() => setView("dashboard")}
      >
        <div className="relative size-10 rounded-xl flex items-center justify-center bg-[#CE0033] shadow-[0_4px_16px_rgba(206,0,51,0.4)] group-hover:shadow-[0_4px_28px_rgba(206,0,51,0.6)] transition-all duration-500">
          <svg viewBox="0 0 100 100" className="size-6">
            <circle cx="50" cy="50" r="38" stroke="white" strokeWidth="10" fill="none" />
            <rect x="43" y="32" width="14" height="14" fill="white" rx="2" />
            <rect x="43" y="52" width="14" height="14" fill="white" rx="2" />
          </svg>
          <div className="absolute inset-0 rounded-xl bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
        <div>
          <div className="font-black text-xl tracking-tighter leading-none flex items-center gap-0.5">
            <span className="text-white">Simplon</span>
            <span className="text-[#CE0033]">.</span>
          </div>
          <div className="label-xs text-zinc-600">Admin System</div>
        </div>
      </div>

      {/* Section label */}
      <div className="label-xs text-zinc-700 mb-3 px-1">Navigation</div>

      {/* Nav */}
      <nav className="flex flex-col gap-1.5">
        <SidebarLink icon={LayoutDashboard} label="Tableau de Bord" active={view === "dashboard"} onClick={() => setView("dashboard")} />
        <SidebarLink icon={GraduationCap}   label="Formations"      active={view === "formations"} onClick={() => setView("formations")} />
        <SidebarLink icon={Calendar}        label="Sessions"         active={view === "sessions"}  onClick={() => setView("sessions")} />
        <SidebarLink icon={Users}           label="Utilisateurs"     active={view === "utilisateurs"} onClick={() => setView("utilisateurs")} />
        <SidebarLink icon={BarChart3}       label="Statistiques"     active={view === "stats"}     onClick={() => setView("stats")} />
        <SidebarLink icon={Settings}        label="Paramètres"       active={view === "settings"}  onClick={() => setView("settings")} />
      </nav>

      {/* Spacer */}
      <div className="flex-1" />

      {/* API Status */}
      <div className="p-4 rounded-2xl bg-white/3 dark:bg-white/[0.03] border border-white/8 dark:border-white/[0.06]">
        <div className="label-xs text-zinc-600 mb-2.5">Build v2.6.1</div>
        <div className="flex items-center gap-2.5">
          <div className={`size-2 rounded-full ${apiOnline ? "bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" : "bg-red-400 shadow-[0_0_6px_rgba(239,68,68,0.8)]"}`} />
          <span className="text-xs font-bold text-zinc-400">
            API : <span className={apiOnline ? "text-emerald-400" : "text-red-400"}>{apiOnline ? "EN LIGNE" : "HORS LIGNE"}</span>
          </span>
        </div>
      </div>
    </div>
  );
}
