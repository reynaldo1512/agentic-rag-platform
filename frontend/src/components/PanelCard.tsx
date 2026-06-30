import type { ReactNode } from "react";

interface PanelCardProps {
  children: ReactNode;
}

/**
 * Contenedor visual base para los paneles del Dashboard.
 */
export function PanelCard({ children }: PanelCardProps) {
  return (
    <div className="rounded-2xl border border-white/5 bg-surface p-8 shadow-[0_0_0_1px_rgba(255,255,255,0.02)]">
      {children}
    </div>
  );
}
