import { PanelCard } from "../components/PanelCard";
import { StatusIndicator } from "../components/StatusIndicator";
import { useBackendStatus } from "../utils/useBackendStatus";

/**
 * Dashboard principal de Agentic RAG Platform.
 *
 * Es la única pantalla de esta iteración. Consulta el estado del
 * Backend (`/health` y `/`) y refleja el resultado en tiempo real.
 */
export function Dashboard() {
  const { connectionState, appInfo, refresh } = useBackendStatus();

  const apiUrl = import.meta.env.VITE_API_URL ?? "—";

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6 py-16 font-body">
      <div className="w-full max-w-md">
        <header className="mb-8 text-center">
          <p className="font-display text-xs uppercase tracking-[0.3em] text-muted">
            Bootstrap · v{appInfo?.version ?? "1.0.0"}
          </p>
          <h1 className="mt-2 font-display text-2xl font-semibold tracking-tight">
            Agentic RAG Platform
          </h1>
        </header>

        <PanelCard>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted">Backend Status</span>
            <StatusIndicator state={connectionState} />
          </div>

          <div className="mt-6 border-t border-white/5 pt-6">
            <dl className="grid grid-cols-2 gap-y-3 text-sm">
              <dt className="text-muted">Application</dt>
              <dd className="text-right font-display text-white">
                {appInfo?.application ?? "—"}
              </dd>

              <dt className="text-muted">Version</dt>
              <dd className="text-right font-display text-white">
                {appInfo?.version ?? "—"}
              </dd>

              <dt className="text-muted">Endpoint</dt>
              <dd className="truncate text-right font-display text-xs text-muted">
                {apiUrl}/health
              </dd>
            </dl>
          </div>

          <button
            onClick={refresh}
            className="mt-6 w-full rounded-lg border border-white/10 py-2 text-xs uppercase tracking-widest text-muted transition hover:border-accent/40 hover:text-accent focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
          >
            Re-check connection
          </button>
        </PanelCard>

        <p className="mt-6 text-center text-xs text-muted">
          Agentic RAG workflow not yet implemented — infrastructure bootstrap only.
        </p>
      </div>
    </main>
  );
}
