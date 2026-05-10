import { useProjects } from "../hooks/projects";
import { useAuth, useLoginRedirect } from "../hooks/auth";
import { NavLink } from "react-router";
import { Plus, AlertCircle, Loader2 } from "lucide-react";

export default function Projects() {
  const { isAuth, loading: authLoading } = useAuth();
  const { data, isLoading, error } = useProjects();
  const login = useLoginRedirect();

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!isAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-4">
        <AlertCircle className="w-12 h-12 text-amber-500" />
        <p className="text-neutral-400">Please, login to see you projects</p>
        <button
          onClick={login}
          className="px-6 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition"
        >
          Login
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center px-6 py-16 gap-8">
      {/* HEADER */}
      <section className="w-full max-w-6xl">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-5xl font-semibold text-shadow-2xs text-shadow-gray-900 dark:text-shadow-gray-400">
              My Projects
            </h1>
            <p className="text-neutral-600 dark:text-neutral-400 mt-2">
              Manage and analyze your projects
            </p>
          </div>
          <NavLink
            to="/projects/new"
            className="
              flex items-center gap-2
              px-6 py-3
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
      </section>

      {/* PROJECTS GRID */}
      <section className="w-full max-w-6xl">
        {isLoading ? (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          </div>
        ) : error ? (
          <div className="flex items-center justify-center py-16 flex-col gap-4">
            <AlertCircle className="w-12 h-12 text-red-500" />
            <p className="text-neutral-400">Error loading projects</p>
          </div>
        ) : !data?.names || data.names.length === 0 ? (
          <div className="flex items-center justify-center py-20 flex-col gap-4">
            <p className="text-neutral-400">You don't have any projects yet</p>
            <NavLink
              to="/projects/new"
              className="px-6 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition"
            >
              Create your first project
            </NavLink>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.names.map((name, idx) => (
              <NavLink
                key={idx}
                to={`/projects/${idx + 1}`}
                className="
                  group
                  p-6
                  rounded-2xl
                  bg-linear-to-br from-blue-500/20 to-blue-700/20
                  dark:from-blue-600/30 dark:to-blue-800/30
                  border border-blue-400/30 dark:border-blue-500/30
                  backdrop-blur-sm
                  hover:from-blue-500/30 hover:to-blue-700/30
                  dark:hover:from-blue-600/40 dark:hover:to-blue-800/40
                  hover:border-blue-400/50 dark:hover:border-blue-500/50
                  transition-all duration-300
                  hover:scale-105
                  hover:shadow-xl hover:shadow-blue-900/20
                  cursor-pointer
                "
              >
                <h3 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition">
                  {name}
                </h3>
                <p className="text-neutral-600 dark:text-neutral-400 text-sm mt-2">
                  Click to open project →
                </p>
              </NavLink>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
