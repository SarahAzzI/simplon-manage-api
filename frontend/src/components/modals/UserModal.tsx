"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { User } from "@/lib/api";
import { ModalWrapper, Field } from "./FormationModal";

const inputCls =
  "w-full bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-3.5 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20 dark:focus:ring-[#CE0033]/15 focus:border-[#CE0033]/30 transition-all text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600";

interface UserModalProps {
  mode: "create" | "edit";
  data: Partial<User>;
  onChange: (d: Partial<User>) => void;
  onSubmit: (e: React.FormEvent) => void;
  onClose: () => void;
}

export function UserModal({ mode, data, onChange, onSubmit, onClose }: UserModalProps) {
  return (
    <ModalWrapper title={mode === "create" ? "Nouvel Utilisateur" : "Éditer Utilisateur"} onClose={onClose}>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Field label="Prénom">
            <input
              required
              value={data.name ?? ""}
              onChange={e => onChange({ ...data, name: e.target.value })}
              className={inputCls}
              placeholder="Ex : Sarah"
            />
          </Field>
          <Field label="Nom">
            <input
              required
              value={data.surname ?? ""}
              onChange={e => onChange({ ...data, surname: e.target.value })}
              className={inputCls}
              placeholder="Ex : Dupont"
            />
          </Field>
        </div>

        <Field label="Adresse email">
          <input
            type="email"
            required
            value={data.email ?? ""}
            onChange={e => onChange({ ...data, email: e.target.value })}
            className={inputCls}
            placeholder="Ex : sarah@simplon.co"
          />
        </Field>

        {mode === "create" && (
          <Field label="Date de naissance">
            <input
              type="date"
              required
              value={data.birth_date ?? ""}
              onChange={e => onChange({ ...data, birth_date: e.target.value })}
              className={inputCls}
            />
          </Field>
        )}

        <Field label="Rôle">
          <select
            value={data.role ?? "Etudiant"}
            onChange={e => onChange({ ...data, role: e.target.value as User["role"] })}
            className={inputCls}
          >
            <option value="Etudiant">Étudiant / Apprenant</option>
            <option value="Formateur">Formateur</option>
            <option value="Administrateur">Administrateur</option>
          </select>
        </Field>

        <div className="flex gap-3 pt-4">
          <Button type="button" variant="ghost" className="flex-1 rounded-2xl border border-zinc-200 dark:border-white/[0.08]" onClick={onClose}>
            Annuler
          </Button>
          <Button type="submit" className="flex-1 rounded-2xl bg-[#CE0033] hover:bg-[#b3002d] text-white shadow-lg shadow-[rgba(206,0,51,0.3)]">
            {mode === "create" ? "Créer" : "Enregistrer"}
          </Button>
        </div>
      </form>
    </ModalWrapper>
  );
}
