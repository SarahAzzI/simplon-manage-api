"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { User, Formation } from "@/lib/api";
import { ModalWrapper, Field } from "./FormationModal";

const inputCls =
  "w-full bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-3.5 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20 dark:focus:ring-[#CE0033]/15 focus:border-[#CE0033]/30 transition-all text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600";

/* ─── Session Modal ─────────────────────────────────── */
interface SessionData {
  formation_id: number;
  formateur_id: number;
  date_debut: string;
  date_fin: string;
  capacite_max: number;
  statut?: string;
}

interface SessionModalProps {
  mode: "create" | "edit";
  data: Partial<SessionData>;
  formations: Formation[];
  formateurs: User[];
  onChange: (d: Partial<SessionData>) => void;
  onSubmit: (e: React.FormEvent) => void;
  onClose: () => void;
}

export function SessionModal({ mode, data, formations, formateurs, onChange, onSubmit, onClose }: SessionModalProps) {
  return (
    <ModalWrapper title={mode === "create" ? "Nouvelle Session" : "Modifier Session"} onClose={onClose}>
      <form onSubmit={onSubmit} className="space-y-4">
        {mode === "create" && (
          <>
            <Field label="Formation">
              <select
                required
                value={data.formation_id ?? 0}
                onChange={e => onChange({ ...data, formation_id: parseInt(e.target.value) })}
                className={inputCls}
              >
                <option value={0}>Sélectionner une formation...</option>
                {formations.map(f => (
                  <option key={f.id} value={f.id}>{f.title}</option>
                ))}
              </select>
            </Field>

            <Field label="Formateur référent">
              <select
                required
                value={data.formateur_id ?? 0}
                onChange={e => onChange({ ...data, formateur_id: parseInt(e.target.value) })}
                className={inputCls}
              >
                <option value={0}>Sélectionner un formateur...</option>
                {formateurs.map(u => (
                  <option key={u.id} value={u.id}>{u.name} {u.surname}</option>
                ))}
              </select>
            </Field>
          </>
        )}

        <div className="grid grid-cols-2 gap-4">
          <Field label="Date de début">
            <input
              type="date"
              required
              value={data.date_debut ?? ""}
              onChange={e => onChange({ ...data, date_debut: e.target.value })}
              className={inputCls}
            />
          </Field>
          <Field label="Date de fin">
            <input
              type="date"
              required
              value={data.date_fin ?? ""}
              onChange={e => onChange({ ...data, date_fin: e.target.value })}
              className={inputCls}
            />
          </Field>
        </div>

        <Field label="Capacité maximale">
          <input
            type="number"
            required
            min={1}
            value={data.capacite_max ?? ""}
            onChange={e => onChange({ ...data, capacite_max: parseInt(e.target.value) })}
            className={inputCls}
            placeholder="Ex : 20"
          />
        </Field>

        {mode === "edit" && (
          <Field label="Statut">
            <select
              value={data.statut ?? "planifiée"}
              onChange={e => onChange({ ...data, statut: e.target.value })}
              className={inputCls}
            >
              <option value="planifiée">Planifiée</option>
              <option value="en_cours">En cours</option>
              <option value="terminée">Terminée</option>
              <option value="annulée">Annulée</option>
            </select>
          </Field>
        )}

        <div className="flex gap-3 pt-4">
          <Button type="button" variant="ghost" className="flex-1 rounded-2xl border border-zinc-200 dark:border-white/[0.08]" onClick={onClose}>
            Annuler
          </Button>
          <Button type="submit" className="flex-1 rounded-2xl bg-[#CE0033] hover:bg-[#b3002d] text-white shadow-lg shadow-[rgba(206,0,51,0.3)]">
            {mode === "create" ? "Planifier" : "Enregistrer"}
          </Button>
        </div>
      </form>
    </ModalWrapper>
  );
}
