/** Single source of truth for backend addresses. Set in .env.local. */
export const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api"
).replace(/\/+$/, "");

/** Origin that serves /reports (chart images), derived from the API URL. */
export const BACKEND_ORIGIN = new URL(API_BASE_URL).origin;

export const MAX_UPLOAD_BYTES = 100 * 1024 * 1024; // matches backend MAX_FILE_SIZE
export const ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".json"] as const;
