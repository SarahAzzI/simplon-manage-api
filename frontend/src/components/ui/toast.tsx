"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface ToastProps {
  id: string
  title?: string
  description?: string
  variant?: "default" | "destructive" | "success"
  onClose: (id: string) => void
}

function Toast({ id, title, description, variant = "default", onClose }: ToastProps) {
  React.useEffect(() => {
    const timer = setTimeout(() => onClose(id), 4000)
    return () => clearTimeout(timer)
  }, [id, onClose])

  return (
    <div
      className={cn(
        "flex items-start gap-3 p-4 rounded-2xl shadow-2xl border animate-slide-up max-w-sm w-full",
        variant === "destructive" && "bg-red-950/90 border-red-800/50 text-red-100 backdrop-blur-xl",
        variant === "success" && "bg-emerald-950/90 border-emerald-800/50 text-emerald-100 backdrop-blur-xl",
        variant === "default" && "bg-zinc-900/90 border-zinc-700/50 text-zinc-100 backdrop-blur-xl dark:bg-zinc-900/90"
      )}
    >
      <div
        className={cn(
          "size-2 rounded-full mt-1.5 shrink-0",
          variant === "destructive" && "bg-red-400",
          variant === "success" && "bg-emerald-400",
          variant === "default" && "bg-zinc-400"
        )}
      />
      <div className="flex-1 min-w-0">
        {title && <p className="text-sm font-bold">{title}</p>}
        {description && <p className="text-xs opacity-80 mt-0.5 leading-relaxed">{description}</p>}
      </div>
      <button
        onClick={() => onClose(id)}
        className="text-white/40 hover:text-white/80 transition-colors text-lg leading-none mt-0.5"
      >
        ×
      </button>
    </div>
  )
}

interface ToastData {
  id: string
  title?: string
  description?: string
  variant?: "default" | "destructive" | "success"
}

interface ToastContextValue {
  toast: (data: Omit<ToastData, "id">) => void
}

const ToastContext = React.createContext<ToastContextValue>({ toast: () => {} })

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastData[]>([])

  const toast = React.useCallback((data: Omit<ToastData, "id">) => {
    const id = Math.random().toString(36).slice(2)
    setToasts(prev => [...prev, { ...data, id }])
  }, [])

  const remove = React.useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed bottom-6 right-6 z-[9999] flex flex-col gap-3 items-end">
        {toasts.map(t => (
          <Toast key={t.id} {...t} onClose={remove} />
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  return React.useContext(ToastContext)
}
