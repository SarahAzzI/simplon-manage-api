"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { X } from "lucide-react"

interface SheetProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  children: React.ReactNode
  side?: "left" | "right"
}

export function Sheet({ open, onOpenChange, children, side = "left" }: SheetProps) {
  // Lock body scroll when open
  React.useEffect(() => {
    if (open) document.body.style.overflow = "hidden"
    else document.body.style.overflow = ""
    return () => { document.body.style.overflow = "" }
  }, [open])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-[150]">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={() => onOpenChange(false)}
      />
      {/* Panel */}
      <div
        className={cn(
          "absolute top-0 h-full w-72 bg-[#0a0a16] border-r border-[rgba(206,0,51,0.15)] shadow-2xl",
          "animate-in duration-300 ease-out",
          side === "left"
            ? "left-0 slide-in-from-left"
            : "right-0 slide-in-from-right"
        )}
      >
        <button
          className="absolute top-5 right-5 text-zinc-400 hover:text-white transition-colors p-1"
          onClick={() => onOpenChange(false)}
        >
          <X size={20} />
        </button>
        {children}
      </div>
    </div>
  )
}
