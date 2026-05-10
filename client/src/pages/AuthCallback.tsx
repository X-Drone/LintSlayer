import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { setToken } from "../hooks/api";

export default function AuthCallback() {
  const [params] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const token = params.get("token");
    const state = params.get("state") || "/";

    if (!token) {
      navigate("/");
      return;
    }

    setToken(token);

    navigate(state, { replace: true });
  }, []);

  return (
    <div className="h-screen flex items-center justify-center text-neutral-500">
      Signing you in...
    </div>
  );
}