/**
 * Tipos relacionados con el estado general del Backend.
 */

export interface HealthStatus {
  status: string;
}

export interface AppInfo {
  application: string;
  version: string;
}

/**
 * Estado de conexión derivado, usado por la UI del Dashboard.
 */
export type BackendConnectionState = "loading" | "online" | "offline";
