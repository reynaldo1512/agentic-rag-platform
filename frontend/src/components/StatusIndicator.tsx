import type { BackendConnectionState } from "../types/health";

interface StatusIndicatorProps {
  state: BackendConnectionState;
}

const STATE_CONFIG: Record<
  BackendConnectionState,
  { label: string; dot: string; ring: string; text: string }
> = {
  loading: {
    label: "Checking",
    dot: "bg-muted",
    ring: "bg-muted",
    text: "text-muted",
  },
  online: {
    label: "Online",
    dot: "bg-accent",
    ring: "bg-accent",
    text: "text-accent",
  },
  offline: {
    label: "Offline",
    dot: "bg-danger",
    ring: "bg-danger",
    text: "text-danger",
  },
};

/**
 * Punto de estado con animación de pulso.
 *
 * Es el elemento "signature" del Dashboard: un latido visual que
 * comunica, sin texto adicional, si el Backend está vivo.
 */
export function StatusIndicator({ state }: StatusIndicatorProps) {
  const config = STATE_CONFIG[state];

  return (
    <div className="flex items-center gap-3">
      <span className="relative flex h-3 w-3">
        {state !== "loading" && (
          <span
            className={`absolute inline-flex h-full w-full animate-ping rounded-full ${config.ring} opacity-40`}
          />
        )}
        <span className={`relative inline-flex h-3 w-3 rounded-full ${config.dot}`} />
      </span>
      <span className={`font-display text-sm uppercase tracking-widest ${config.text}`}>
        {config.label}
      </span>
    </div>
  );
}
