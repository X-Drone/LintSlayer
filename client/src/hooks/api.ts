const API_BASE = import.meta.env.VITE_BACKEND_URL;
const TOKEN_KEY = "auth_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
}

export async function request<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options?.headers as Record<string, string> || {}),
  };

  // Добавляем Authorization header если есть токен
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw error;
  }

  return res.json();
}

export const queryKeys = {
  projects: ["projects"] as const,

  project: (id: number) => ["projects", id] as const,

  analyses: (projectId: number) =>
    ["projects", projectId, "analyses"] as const,

  analysis: (projectId: number, runId: number) =>
    ["projects", projectId, "analyses", runId] as const,
};

export async function validateAuth(token: string) {
  const res = await fetch(
    `${import.meta.env.VITE_AUTH_URL_SERVER}/auth/verify`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    }
  );

  if (!res.ok) return null;

  return res.json();
}
