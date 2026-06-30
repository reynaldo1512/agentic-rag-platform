import { useCallback, useEffect, useState } from "react";

import { fetchAppInfo, fetchHealth } from "../services/healthService";
import type { AppInfo, BackendConnectionState } from "../types/health";

interface UseBackendStatusResult {
  connectionState: BackendConnectionState;
  appInfo: AppInfo | null;
  refresh: () => void;
}

/**
 * Hook que consulta el estado del Backend (`/` y `/health`) y expone
 * el resultado como estado de conexión derivado para la UI.
 */
export function useBackendStatus(): UseBackendStatusResult {
  const [connectionState, setConnectionState] =
    useState<BackendConnectionState>("loading");
  const [appInfo, setAppInfo] = useState<AppInfo | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = useCallback(() => {
    setRefreshKey((key) => key + 1);
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function checkBackend(): Promise<void> {
      setConnectionState("loading");

      try {
        const [health, info] = await Promise.all([fetchHealth(), fetchAppInfo()]);

        if (!isMounted) return;

        if (health.status === "ok") {
          setConnectionState("online");
          setAppInfo(info);
        } else {
          setConnectionState("offline");
        }
      } catch {
        if (isMounted) {
          setConnectionState("offline");
          setAppInfo(null);
        }
      }
    }

    void checkBackend();

    return () => {
      isMounted = false;
    };
  }, [refreshKey]);

  return { connectionState, appInfo, refresh };
}
