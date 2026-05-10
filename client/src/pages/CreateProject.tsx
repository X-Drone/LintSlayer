import { useState } from "react";
import { useNavigate } from "react-router";
import { useCreateProject } from "../hooks/projects";
import { ArrowLeft, Loader2, Code2 } from "lucide-react";

type CreateMode = "url" | "code";

export default function CreateProject() {
  const navigate = useNavigate();
  const createProjectMutation = useCreateProject();

  const [mode, setMode] = useState<CreateMode>("url");
  const [projectName, setProjectName] = useState("");
  const [repoUrl, setRepoUrl] = useState("");
  const [code, setCode] = useState("");
  const [ext, setExt] = useState("js");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!projectName.trim()) {
      alert("Please specify a project name");
      return;
    }

    const data: any = {
      name: projectName.trim(),
    };

    if (mode === "url") {
      if (!repoUrl.trim()) {
        alert("Please specify the Git repository URL");
        return;
      }
      data.repo_url = repoUrl.trim();
    } else {
      if (!code.trim()) {
        alert("Please specify the code to analyze");
        return;
      }
      data.content = code;
      data.ext = ext;
    }

    try {
      await createProjectMutation.mutateAsync(data);
      navigate("/projects");
    } catch (err: any) {
      alert(`Error: ${err.detail || "Failed to create project"}`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center px-6 py-16 gap-12">
      {/* HEADER */}
      <section className="w-full max-w-2xl">
        <button
          onClick={() => navigate("/projects")}
          className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200 transition mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Return to Projects
        </button>

        <h1 className="text-5xl font-semibold text-shadow-2xs text-shadow-gray-900 dark:text-shadow-gray-400 mb-3">
          Create Project
        </h1>
        <p className="text-neutral-600 dark:text-neutral-400">
          Choose how you want to create your project: from a Git repository or by pasting code directly.
        </p>
      </section>

      {/* FORM */}
      <section className="w-full max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* MODE SELECTOR */}
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setMode("url")}
              className={`
                flex-1 py-4 px-6 rounded-xl font-semibold transition-all
                ${
                  mode === "url"
                    ? "bg-linear-to-br from-blue-500 to-blue-700 text-white shadow-lg shadow-blue-900/30"
                    : "bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-300 dark:hover:bg-neutral-600"
                }
              `}
            >
              📦 Git repository
            </button>
            <button
              type="button"
              onClick={() => setMode("code")}
              className={`
                flex-1 py-4 px-6 rounded-xl font-semibold transition-all
                ${
                  mode === "code"
                    ? "bg-linear-to-br from-blue-500 to-blue-700 text-white shadow-lg shadow-blue-900/30"
                    : "bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-300 dark:hover:bg-neutral-600"
                }
              `}
            >
              <Code2 className="w-5 h-5 inline mr-2" />
              Text code
            </button>
          </div>

          {/* PROJECT NAME */}
          <div>
            <label className="block text-neutral-700 dark:text-neutral-300 font-semibold mb-2">
              Project Name
            </label>
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="For example: MyCoolApp"
              className="
                w-full px-4 py-3 rounded-lg
                bg-neutral-100 dark:bg-neutral-800
                border border-neutral-300 dark:border-neutral-600
                text-neutral-900 dark:text-neutral-100
                placeholder-neutral-500 dark:placeholder-neutral-400
                focus:outline-none focus:ring-2 focus:ring-blue-500
                transition
              "
            />
          </div>

          {/* MODE-SPECIFIC FIELDS */}
          {mode === "url" ? (
            <div>
              <label className="block text-neutral-700 dark:text-neutral-300 font-semibold mb-2">
                Git Repository URL
              </label>
              <input
                type="url"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="https://github.com/user/repo.git"
                className="
                  w-full px-4 py-3 rounded-lg
                  bg-neutral-100 dark:bg-neutral-800
                  border border-neutral-300 dark:border-neutral-600
                  text-neutral-900 dark:text-neutral-100
                  placeholder-neutral-500 dark:placeholder-neutral-400
                  focus:outline-none focus:ring-2 focus:ring-blue-500
                  transition
                "
              />
            </div>
          ) : (
            <>
              <div>
                <label className="block text-neutral-700 dark:text-neutral-300 font-semibold mb-2">
                  File Extension
                </label>
                <select
                  value={ext}
                  onChange={(e) => setExt(e.target.value)}
                  className="
                    w-full px-4 py-3 rounded-lg
                    bg-neutral-100 dark:bg-neutral-800
                    border border-neutral-300 dark:border-neutral-600
                    text-neutral-900 dark:text-neutral-100
                    focus:outline-none focus:ring-2 focus:ring-blue-500
                    transition
                  "
                >
                  <option value="js">JavaScript (.js)</option>
                  <option value="ts">TypeScript (.ts)</option>
                  <option value="jsx">JSX (.jsx)</option>
                  <option value="tsx">TSX (.tsx)</option>
                  <option value="py">Python (.py)</option>
                  <option value="java">Java (.java)</option>
                  <option value="cpp">C++ (.cpp)</option>
                  <option value="c">C (.c)</option>
                </select>
              </div>
              <div>
                <label className="block text-neutral-700 dark:text-neutral-300 font-semibold mb-2">
                  Text Code
                </label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Paste your code here..."
                  rows={12}
                  className="
                    w-full px-4 py-3 rounded-lg
                    bg-neutral-100 dark:bg-neutral-800
                    border border-neutral-300 dark:border-neutral-600
                    text-neutral-900 dark:text-neutral-100 font-mono text-sm
                    placeholder-neutral-500 dark:placeholder-neutral-400
                    focus:outline-none focus:ring-2 focus:ring-blue-500
                    transition
                  "
                />
              </div>
            </>
          )}

          {/* SUBMIT BUTTON */}
          <button
            type="submit"
            disabled={createProjectMutation.isPending}
            className="
              w-full py-4 rounded-xl
              bg-linear-to-br from-blue-500 to-blue-700
              text-white font-semibold
              shadow-lg shadow-blue-900/30
              hover:scale-105 hover:shadow-xl
              disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
              transition-all duration-300
              flex items-center justify-center gap-2
            "
          >
            {createProjectMutation.isPending && (
              <Loader2 className="w-5 h-5 animate-spin" />
            )}
            {createProjectMutation.isPending ? "Creating..." : "Create Project"}
          </button>
        </form>
      </section>
    </div>
  );
}
