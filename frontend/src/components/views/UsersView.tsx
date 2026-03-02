"use client";

import React from "react";
import { Users, MoreVertical } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { User } from "@/lib/api";

const ROLE_COLOR: Record<string, string> = {
  Formateur: "bg-[#CE0033] text-white",
  Administrateur: "bg-violet-500/15 text-violet-400",
  Etudiant: "bg-zinc-200 text-zinc-700 dark:bg-white/8 dark:text-zinc-400",
};

const ROLE_LABEL: Record<string, string> = {
  Formateur: "Formateur",
  Administrateur: "Admin",
  Etudiant: "Étudiant",
};

interface UsersViewProps {
  users: User[];
  totalUsers: number;
  searchQuery: string;
  onEdit: (u: User) => void;
  onDelete: (u: User) => void;
}

export function UsersView({ users, totalUsers, searchQuery, onEdit, onDelete }: UsersViewProps) {
  const filtered = users.filter(u => {
    const q = searchQuery.toLowerCase();
    return (
      u.name?.toLowerCase().includes(q) ||
      u.surname?.toLowerCase().includes(q) ||
      u.email?.toLowerCase().includes(q) ||
      u.role?.toLowerCase().includes(q)
    );
  });

  return (
    <Card className="border-none glass-card animate-in fade-in duration-500">
      <CardHeader className="p-7 pb-5 border-b border-zinc-100 dark:border-white/[0.04]">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="heading-lg">Annuaire Simplon</CardTitle>
            <CardDescription className="text-zinc-500 dark:text-zinc-600 mt-1">
              {filtered.length} / {totalUsers} utilisateur{totalUsers > 1 ? "s" : ""}
            </CardDescription>
          </div>
          <Button
            variant="outline"
            className="rounded-full label-xs border-zinc-200 dark:border-white/[0.1] hover:bg-zinc-50 dark:hover:bg-white/[0.04] hidden sm:flex"
          >
            Exporter CSV
          </Button>
        </div>
      </CardHeader>

      <CardContent className="p-4">
        {filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="size-16 rounded-2xl bg-zinc-100 dark:bg-white/5 flex items-center justify-center mb-4">
              <Users size={32} className="text-zinc-300 dark:text-zinc-700" />
            </div>
            <p className="text-sm text-zinc-400">
              {searchQuery ? `Aucun résultat pour "${searchQuery}"` : "Aucun utilisateur."}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
            {filtered.map((user) => {
              const initials = `${user.name?.[0] ?? ""}${user.surname?.[0] ?? ""}`.toUpperCase();
              const roleColor = ROLE_COLOR[user.role] ?? ROLE_COLOR.Etudiant;
              return (
                <div
                  key={user.id}
                  className="p-4 rounded-2xl border border-zinc-100 dark:border-white/[0.04] hover:bg-zinc-50 dark:hover:bg-white/[0.03] hover:border-zinc-200 dark:hover:border-white/[0.08] transition-all flex items-center gap-4 group"
                >
                  {/* Avatar */}
                  <div className="relative shrink-0">
                    <div className="size-12 rounded-2xl bg-gradient-to-tr from-zinc-900 to-zinc-700 dark:from-[#CE0033]/30 dark:to-[#CE0033]/10 flex items-center justify-center text-white font-black text-base shadow-md">
                      {initials}
                    </div>
                    {!user.is_active && (
                      <div className="absolute -top-1 -right-1 size-3.5 bg-[#CE0033] rounded-full border-2 border-white dark:border-[#080810]" />
                    )}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-zinc-900 dark:text-zinc-100 group-hover:text-[#CE0033] transition-colors text-sm uppercase italic truncate">
                      {user.name} {user.surname}
                    </div>
                    <div className="text-xs text-zinc-400 truncate mb-1.5">{user.email}</div>
                    <span className={`inline-block label-xs px-2 py-0.5 rounded-md ${roleColor}`}>
                      {ROLE_LABEL[user.role] ?? user.role}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-1 shrink-0">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="size-7 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/[0.06]"
                      onClick={() => onEdit(user)}
                    >
                      <MoreVertical size={14} />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="size-7 rounded-lg text-zinc-300 hover:text-[#CE0033] hover:bg-red-50 dark:hover:bg-[#CE0033]/10"
                      onClick={() => onDelete(user)}
                    >
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                      </svg>
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
