import axios from "axios";

/**
 * URL base del Backend, leída desde variables de entorno de Vite.
 *
 * No se utilizan URLs hardcodeadas: el valor proviene de `VITE_API_URL`
 * (ver `.env.example`).
 */
const baseURL = import.meta.env.VITE_API_URL;

if (!baseURL) {
  // eslint-disable-next-line no-console
  console.warn(
    "VITE_API_URL no está definida. Configúrala en tu archivo .env (ver .env.example)."
  );
}

export const apiClient = axios.create({
  baseURL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});
