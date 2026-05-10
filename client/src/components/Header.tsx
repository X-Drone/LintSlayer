import { Home, LogOut, User, LogIn, List, Plus, Loader2 } from "lucide-react";
import { NavLink, useNavigate } from "react-router";
import NavButton from "../components/NavButton";
import { useAuth, useLoginRedirect } from "../hooks/auth";
import { logout } from "../hooks/api";

export default function Header() {
    const { isAuth, loading } = useAuth();
    const login = useLoginRedirect();
    const navigate = useNavigate();

    const handleLogout = async () => {
        logout();
        navigate("/");
        window.location.reload();
    };

    return (
        <header className="h-20 sticky top-0 z-50
            backdrop-blur-sm
            bg-black/10 dark:bg-white/10
            border-b border-white/10 shadow-lg shadow-black/20">
            <div className="h-full px-4 flex items-center justify-between">
                
                {/* LEFT: Logo + Main nav */}
                <div className="flex items-center gap-2">
                <nav className="flex items-center p-5">
                    <NavButton to="/" icon={Home} />
                </nav>

                <h2 className="text-3xl font-semibold px-3 opacity-90">
                    LS
                </h2>
                </div>

                {/* CENTER: big ANALYSE button */}
                <div className="absolute left-1/2 -translate-x-1/2">
                    <NavLink
                        to="/projects/new"
                        className="
                        flex items-center gap-2
                        px-6 py-2.5
                        rounded-xl
                        bg-linear-to-br from-blue-500 to-blue-700
                        text-white font-semibold
                        shadow-lg shadow-blue-900/30
                        transition-all duration-300

                        hover:scale-105 hover:shadow-xl
                        active:scale-95
                        "
                    >
                        <Plus className="w-5 h-5" />
                        New Project
                    </NavLink>
                    </div>

                {/* RIGHT: User actions */}
                <nav className="flex items-center gap-1">
                    {loading ? (
                        <div className="px-3 py-2 flex items-center text-neutral-500">
                            <Loader2 className="w-4 h-4 animate-spin" />
                        </div>
                    ) : isAuth ? (
                        <>
                        <NavButton to="/projects" icon={List} />
                        <NavButton to={`${import.meta.env.VITE_AUTH_URL_CLIENT}/profile`} icon={User} />
                        <button
                            onClick={handleLogout}
                            className="
                                rounded-lg p-2 text-slate-600 hover:bg-slate-200 hover:text-slate-900
                                flex items-center gap-2">
                            <LogOut className="w-4 h-4" />
                            Logout
                        </button>
                        </>
                    ) : (
                        <button
                        onClick={login}
                        className="
                            px-4 py-2 rounded-lg
                            bg-blue-600 text-white
                            hover:bg-blue-700 transition
                            flex items-center gap-2
                        "
                        >
                        <LogIn className="w-4 h-4" />
                        Login
                        </button>
                    )}
                </nav>
            </div>
        </header>
    );
}
