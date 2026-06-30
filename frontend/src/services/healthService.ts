import { apiClient } from "../api/client";
import type { AppInfo, HealthStatus } from "../types/health";

/**
 * Capa de servicios para el dominio "health".
 *
 * Los componentes React nunca llaman a Axios directamente: siempre
 * pasan por estas funciones, que centralizan la comunicación HTTP
 * con el Backend.
 */

export async function fetchHealth(): Promise<HealthStatus> {
  const { data } = await apiClient.get<HealthStatus>("/health");
  return data;
}

export async function fetchAppInfo(): Promise<AppInfo> {
  const { data } = await apiClient.get<AppInfo>("/");
  return data;
}
