"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { Formation } from "@/lib/api";

interface ModalWrapperProps {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

export function ModalWrapper({ title, onClose, children }: ModalWrapperProps) {
  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div className="bg-white dark:bg-[#0d0d1f] w-full max-w-lg rounded-3xl p-8 shadow-2xl border border-zinc-100 dark:border-[rgba(206,0,51,0.15)] animate-in zoom-in-95 duration-200 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center gap-3 mb-7">
          <div className="size-1.5 rounded-full bg-[#CE0033]" />
          <h3 className="heading-md font-black uppercase italic text-zinc-900 dark:text-zinc-50">
            {title}
          </h3>
        </div>
        {children}
      </div>
    </div>
  );
}

interface FieldProps {
  label: string;
  children: React.ReactNode;
}

export function Field({ label, children }: FieldProps) {
  return (
    <div>
      <label className="label-xs text-zinc-400 block mb-1.5">{label}</label>
      {children}
    </div>
  );
}

const inputCls =
  "w-full bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-3.5 text-sm outline-none focus:ring-2 focus:ring-[#CE0033]/20 dark:focus:ring-[#CE0033]/15 focus:border-[#CE0033]/30 transition-all text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600";

/* ─── Formation Modal ──────────────────────────────── */
interface FormationModalProps {
  mode: "create" | "edit";
  data: Partial<Formation>;
  onChange: (d: Partial<Formation>) => void;
  onSubmit: (e: React.FormEvent) => void;
  onClose: () => void;
}

export function FormationModal({ mode, data, onChange, onSubmit, onClose }: FormationModalProps) {
  return (
    <ModalWrapper title={mode === "create" ? "Nouvelle Formation" : "Éditer Formation"} onClose={onClose}>
      <form onSubmit={onSubmit} className="space-y-4">
        <Field label="Titre de la formation">
          <input
            required
            value={data.title ?? ""}
            onChange={e => onChange({ ...data, title: e.target.value })}
            className={inputCls}
            placeholder="Ex : Développeur Web Full Stack"
          />
        </Field>

        <Field label="Description">
          <textarea
            required
            rows={3}
            value={data.description ?? ""}
            onChange={e => onChange({ ...data, description: e.target.value })}
            className={inputCls}
            placeholder="Décrivez la formation..."
          />
        </Field>

        <div className="grid grid-cols-2 gap-4">
          <Field label="Durée (en mois)">
            <input
              type="number"
              min={1}
              value={data.duration ?? ""}
              onChange={e => onChange({ ...data, duration: parseInt(e.target.value) })}
              className={inputCls}
              placeholder="Ex : 6"
            />
          </Field>
          <Field label="Niveau">
            <select
              value={data.level ?? "Bac+2"}
              onChange={e => onChange({ ...data, level: e.target.value as Formation["level"] })}
              className={inputCls}
            >
              <option value="débutant">Débutant</option>
              <option value="intermédiaire">Intermédiaire</option>
              <option value="avancé">Avancé</option>
              <option value="Bac+2">Bac+2</option>
              <option value="Bac+3">Bac+3</option>
              <option value="Bac+5">Bac+5</option>
            </select>
          </Field>
        </div>

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
