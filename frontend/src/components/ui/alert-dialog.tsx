"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "./button"

interface AlertDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description?: string
  confirmLabel?: string
  cancelLabel?: string
  onConfirm: () => void
  variant?: "destructive" | "default"
}

export function AlertDialog({
  open,
  onOpenChange,
  title,
  description,
  confirmLabel = "Confirmer",
  cancelLabel = "Annuler",
  onConfirm,
  variant = "destructive",
}: AlertDialogProps) {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={() => onOpenChange(false)}
      />
      {/* Dialog */}
      <div
        className={cn(
          "relative z-10 w-full max-w-md rounded-3xl p-8 shadow-2xl border animate-in zoom-in-95 duration-200",
          "bg-white dark:bg-zinc-950 border-zinc-100 dark:border-zinc-800"
        )}
      >
        <div className={cn(
          "size-12 rounded-2xl flex items-center justify-center mb-5",
          variant === "destructive" ? "bg-red-50 dark:bg-red-950/40" : "bg-zinc-100 dark:bg-zinc-800"
        )}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
            className={variant === "destructive" ? "text-[#CE0033]" : "text-zinc-600"}>
            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
        </div>

        <h3 className="text-lg font-black uppercase tracking-tight text-zinc-900 dark:text-zinc-50 mb-2">
          {title}
        </h3>
        {description && (
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8 leading-relaxed">
            {description}
          </p>
        )}

        <div className="flex gap-3">
          <Button
            variant="ghost"
            className="flex-1 rounded-2xl border border-zinc-200 dark:border-zinc-800"
            onClick={() => onOpenChange(false)}
          >
            {cancelLabel}
          </Button>
          <Button
            className={cn(
              "flex-1 rounded-2xl font-bold",
              variant === "destructive"
                ? "bg-[#CE0033] hover:bg-[#b3002d] text-white"
                : "bg-zinc-900 dark:bg-white text-white dark:text-black"
            )}
            onClick={() => { onConfirm(); onOpenChange(false) }}
          >
            {confirmLabel}
          </Button>
        </div>
      </div>
    </div>
  )
}
