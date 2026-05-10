import { useParams, useNavigate } from "react-router";
import { useProject } from "../hooks/projects";
import { useAnalyses, useAnalysis, useRunAnalysis } from "../hooks/analyses";
import { useAuth, useLoginRedirect } from "../hooks/auth";
import type { IssueResponse, AnalysisRunResponse } from "../hooks/types";
import {
  ArrowLeft,
  AlertCircle,
  Loader2,
  Zap,
  CheckCircle,
  AlertTriangle,
  Clock,
  FileText,
} from "lucide-react";
import { useState, useMemo } from "react";

export default function ProjectDetail() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { isAuth, loading: authLoading } = useAuth();
  const login = useLoginRedirect();

  const id = projectId ? parseInt(projectId) : 0;

  const { data: project, isLoading: projectLoading, error: projectError } = useProject(id);
  const { data: analyses, isLoading: analysesLoading } = useAnalyses(id);
  const lastAnalysisId = useMemo(() => {
    if (!analyses?.length) return undefined;
    return [...analyses].sort((a, b) => {
      const tA = a.timestamp ? new Date(a.timestamp).getTime() : 0;
      const tB = b.timestamp ? new Date(b.timestamp).getTime() : 0;
      return tB - tA;
    })[0]?.id;
  }, [analyses]);
  const { data: lastAnalysis, isLoading: lastAnalysisLoading } = useAnalysis(
    id,
    lastAnalysisId
  );

  const runAnalysisMutation = useRunAnalysis(id);

  const availableAnalysers = ["Regex Patterns", "Complexity", "Security", "PyLint", "Flake8", "Pyright", "ESLint", "TSLint", "Prettier"];
  const [selectedAnalysers, setSelectedAnalysers] = useState<string[]>(availableAnalysers);

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
        <p className="text-neutral-400">Login to the account to access</p>
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
        <button
          onClick={() => navigate("/projects")}
          className="flex items-center gap-2 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200 transition mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Return to Projects
        </button>

        {projectLoading ? (
          <div className="flex items-center gap-4">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
            <p className="text-neutral-400">Loading project...</p>
          </div>
        ) : projectError ? (
          <div className="flex items-center gap-4">
            <AlertCircle className="w-8 h-8 text-red-500" />
            <p className="text-neutral-400">Error loading project</p>
          </div>
        ) : project ? (
          <div>
            <h1 className="text-5xl font-semibold text-shadow-2xs text-shadow-gray-900 dark:text-shadow-gray-400 mb-2">
              {project.name}
            </h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Owner: <span className="font-semibold">{project.owner}</span>
            </p>
            <p className="text-neutral-600 dark:text-neutral-400">
              Files: <span className="font-semibold">{project.files.length}</span>
            </p>
          </div>
        ) : null}
      </section>

      {/* CONTENT GRID */}
      <section className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* LEFT: RUN ANALYSIS & FILES */}
        <div className="lg:col-span-1 flex flex-col gap-8">
          {/* RUN ANALYSIS CARD */}
          <div className="p-8 rounded-2xl bg-linear-to-br from-blue-500/20 to-blue-700/20 dark:from-blue-600/30 dark:to-blue-800/30 border border-blue-400/30 dark:border-blue-500/30 backdrop-blur-sm">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-6">
              Start Analysis
            </h2>

            {/* ANALYSERS SELECTOR */}
            <div className="space-y-3 mb-6">
              {availableAnalysers.map((analyser) => (
                <label key={analyser} className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedAnalysers.includes(analyser)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedAnalysers([...selectedAnalysers, analyser]);
                      } else {
                        setSelectedAnalysers(
                          selectedAnalysers.filter((a) => a !== analyser)
                        );
                      }
                    }}
                    className="w-5 h-5 rounded border-neutral-400 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-neutral-700 dark:text-neutral-300">{analyser}</span>
                </label>
              ))}
            </div>

            {/* RUN BUTTON */}
            <button
              onClick={() => {
                if (selectedAnalysers.length === 0) {
                  alert("Choose at least one analyser");
                  return;
                }
                runAnalysisMutation.mutate(selectedAnalysers);
              }}
              disabled={runAnalysisMutation.isPending || selectedAnalysers.length === 0}
              className="
                w-full py-3 rounded-lg
                bg-linear-to-br from-blue-500 to-blue-700
                text-white font-semibold
                shadow-lg shadow-blue-900/30
                hover:scale-105 hover:shadow-xl
                disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
                transition-all duration-300
                flex items-center justify-center gap-2
              "
            >
              {runAnalysisMutation.isPending && (
                <Loader2 className="w-5 h-5 animate-spin" />
              )}
              <Zap className="w-5 h-5" />
              {runAnalysisMutation.isPending ? "Analyzing..." : "Start Analysis"}
            </button>
          </div>

          {/* FILES CARD */}
          <div className="p-6 rounded-2xl bg-linear-to-br from-neutral-500/10 to-neutral-700/10 dark:from-neutral-600/20 dark:to-neutral-800/20 border border-neutral-400/20 dark:border-neutral-500/20 backdrop-blur-sm">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5" />
                Files
            </h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {project?.files && project.files.length > 0 ? (
                project.files.map((file, idx) => (
                  <div
                    key={idx}
                    className="text-sm text-neutral-600 dark:text-neutral-400 truncate hover:text-neutral-900 dark:hover:text-neutral-200 transition"
                    title={file}
                  >
                    📄 {file}
                  </div>
                ))
              ) : (
                <p className="text-neutral-500">No files</p>
              )}
            </div>
          </div>
        </div>

        {/* RIGHT: ANALYSIS RESULTS */}
        <div className="lg:col-span-2">
          {analysesLoading ? (
            <div className="p-8 rounded-2xl bg-linear-to-br from-neutral-500/10 to-neutral-700/10 border border-neutral-400/20 flex items-center justify-center h-96">
              <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
            </div>
          ) : !analyses || analyses.length === 0 ? (
            <div className="p-8 rounded-2xl bg-linear-to-br from-neutral-500/10 to-neutral-700/10 border border-neutral-400/20 flex items-center justify-center h-96 flex-col gap-4">
              <AlertCircle className="w-12 h-12 text-neutral-400" />
              <p className="text-neutral-400">Analysis has not been run yet</p>
            </div>
          ) : lastAnalysisLoading ? (
            <div className="p-8 rounded-2xl bg-linear-to-br from-neutral-500/10 to-neutral-700/10 border border-neutral-400/20 flex items-center justify-center h-96">
              <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
            </div>
          ) : lastAnalysis ? (
            <div className="space-y-6">
              {/* LATEST ANALYSIS HEADER */}
              <div className="p-6 rounded-2xl bg-linear-to-br from-blue-500/20 to-blue-700/20 dark:from-blue-600/30 dark:to-blue-800/30 border border-blue-400/30 dark:border-blue-500/30 backdrop-blur-sm">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
                    Last Analysis
                  </h3>
                  <div className="flex items-center gap-2">
                    {lastAnalysis.status === "running" && (
                      <div className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400">
                        <Clock className="w-5 h-5 animate-spin" />
                        <span>In Progress</span>
                      </div>
                    )}
                    {lastAnalysis.status === "completed" && (
                      <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                        <CheckCircle className="w-5 h-5" />
                        <span>Completed</span>
                      </div>
                    )}
                    {lastAnalysis.status === "failed" && (
                      <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
                        <AlertTriangle className="w-5 h-5" />
                        <span>Failed</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-neutral-600 dark:text-neutral-400">Analysis ID</p>
                    <p className="font-semibold text-neutral-900 dark:text-neutral-100">
                      #{lastAnalysis.id}
                    </p>
                  </div>
                  <div>
                    <p className="text-neutral-600 dark:text-neutral-400">Timestamp</p>
                    <p className="font-semibold text-neutral-900 dark:text-neutral-100">
                      {lastAnalysis.timestamp
                        ? new Date(lastAnalysis.timestamp).toLocaleString("ru-RU")
                        : "-"}
                    </p>
                  </div>
                </div>
              </div>

              {/* ISSUES LIST */}
              {lastAnalysis.issues && lastAnalysis.issues.length > 0 ? (
                <div className="p-6 rounded-2xl bg-linear-to-br from-amber-500/10 to-red-700/10 border border-amber-400/30 backdrop-blur-sm">
                  <h4 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
                    Found Issues ({lastAnalysis.issues.length})
                  </h4>

                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {lastAnalysis.issues.map((issue: IssueResponse, idx: number) => (
                      <div
                        key={idx}
                        className="p-4 rounded-lg bg-neutral-100/50 dark:bg-neutral-800/50 border border-neutral-300/50 dark:border-neutral-600/50"
                      >
                        <div className="flex items-start gap-3">
                          <div
                            className={`shrink-0 w-2 h-2 rounded-full mt-2 ${
                              issue.severity === "critical"
                                ? "bg-red-600"
                                : issue.severity === "high"
                                  ? "bg-orange-600"
                                  : issue.severity === "medium"
                                    ? "bg-yellow-600"
                                    : "bg-blue-600"
                            }`}
                          />
                          <div className="flex-1">
                            <div className="flex items-center justify-between gap-2 mb-1">
                              <p className="font-semibold text-neutral-900 dark:text-neutral-100">
                                {issue.message}
                              </p>
                              <span
                                className={`text-xs font-semibold px-2 py-1 rounded ${
                                  issue.severity === "critical"
                                    ? "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400"
                                    : issue.severity === "high"
                                      ? "bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400"
                                      : issue.severity === "medium"
                                        ? "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400"
                                        : "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400"
                                }`}
                              >
                                {issue.severity.toUpperCase()}
                              </span>
                            </div>
                            <p className="text-sm text-neutral-600 dark:text-neutral-400">
                              {issue.file_path}:{issue.line_start}
                              {issue.line_end !== issue.line_start
                                ? `-${issue.line_end}`
                                : ""}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="p-8 rounded-2xl bg-linear-to-br from-green-500/10 to-emerald-700/10 border border-green-400/30 flex items-center justify-center gap-4">
                  <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
                  <p className="text-neutral-700 dark:text-neutral-300 font-semibold">
                    Theres no issues! ✨
                  </p>
                </div>
              )}
            </div>
          ) : null}
        </div>
      </section>

      {/* RECENT ANALYSES */}
      {analyses && analyses.length > 1 && (
        <section className="w-full max-w-6xl">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            History
          </h2>
          <div className="space-y-3">
            {analyses.slice(1, 6).map((analysis: AnalysisRunResponse) => (
              <div
                key={analysis.id}
                className="p-4 rounded-lg bg-linear-to-br from-neutral-500/10 to-neutral-700/10 border border-neutral-400/20 flex items-center justify-between"
              >
                <div>
                  <p className="font-semibold text-neutral-900 dark:text-neutral-100">
                    Analysis run #{analysis.id}
                  </p>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400">
                    {analysis.timestamp
                      ? new Date(analysis.timestamp).toLocaleString("ru-RU")
                      : "-"}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {analysis.status === "running" && (
                    <div className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400">
                      <Clock className="w-5 h-5 animate-spin" />
                      <span className="text-sm">In Progress</span>
                    </div>
                  )}
                  {analysis.status === "completed" && (
                    <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                      <CheckCircle className="w-5 h-5" />
                      <span className="text-sm">Completed</span>
                    </div>
                  )}
                  {analysis.status === "failed" && (
                    <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
                      <AlertTriangle className="w-5 h-5" />
                      <span className="text-sm">Failed</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
