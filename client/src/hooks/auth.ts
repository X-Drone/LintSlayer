import { useEffect, useState } from "react";
import { getToken, logout, validateAuth } from "./api";
import { useLocation } from "react-router";

type AuthState = {
  isAuth: boolean;
  username: string | null;
  loading: boolean;
};

export function useAuth(): AuthState {
  const [state, setState] = useState<AuthState>({
    isAuth: false,
    username: null,
    loading: true,
  });

  useEffect(() => {
    const token = getToken();

    if (!token) {
      setState({
        isAuth: false,
        username: null,
        loading: false,
      });
      return;
    }

    (async () => {
      try {
        const data = await validateAuth(token);

        if (!data) {
          setState({
            isAuth: false,
            username: null,
            loading: false,
          });
          
          logout();
          window.location.reload();
          return;
        }

        setState({
          isAuth: true,
          username: data.username,
          loading: false,
        });
      } catch {
        setState({
          isAuth: false,
          username: null,
          loading: false,
        });
      }
    })();
  }, []);

  return state;
}

export function useLoginRedirect() {
  const location = useLocation();

  return () => {
    const authUrl = import.meta.env.VITE_AUTH_URL_CLIENT;

    // полный путь (включая query)
    const returnTo = location.pathname + location.search;

    const redirectUrl = `${authUrl}` +
      `?redirect=${encodeURIComponent(window.location.origin + "/auth/callback")}` +
      `&state=${encodeURIComponent(returnTo)}`;

    window.location.href = redirectUrl;
  };
}
