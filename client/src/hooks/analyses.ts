import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { queryKeys, request } from "./api";
import type { GetAnalyseResponse, GetAnalysesResponse, RunAnalyseResponse } from "./types";

export function useAnalyses(projectId: number) {
  return useQuery({
    queryKey: queryKeys.analyses(projectId),
    queryFn: () =>
      request<GetAnalysesResponse>(
        `/projects/${projectId}/analyses`
      ),
    enabled: !!projectId,
  });
}

export function useAnalysis(
  projectId: number,
  runId?: number
) {
  return useQuery<GetAnalyseResponse>({
    queryKey: queryKeys.analysis(projectId, runId || 0),
    queryFn: () =>
      request<GetAnalyseResponse>(
        `/projects/${projectId}/analyses/${runId}`
      ),
    enabled: !!projectId && !!runId,

    refetchInterval: (query) =>
      query.state.data?.status === "running" ? 2000 : false,
  });
}

export function useRunAnalysis(projectId: number) {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: (analysers: string[]) =>
      request<RunAnalyseResponse>(
        `/projects/${projectId}/analyse`,
        {
          method: "POST",
          body: JSON.stringify(analysers),
        }
      ),
      
    onMutate: async (_analysers) => {
      await qc.cancelQueries({
        queryKey: queryKeys.analyses(projectId),
      });

      const prev = qc.getQueryData<GetAnalysesResponse>(
        queryKeys.analyses(projectId)
      );

      qc.setQueryData<GetAnalysesResponse>(
        queryKeys.analyses(projectId),
        (old = []) => [
          ...old,
          {
            id: 0, // временный ID
            project_id: projectId,
            status: "pending",
            timestamp: new Date().toISOString(),
          },
        ]
      );

      return { prev };
    },

    onError: (_err, _vars, ctx) => {
      if (ctx?.prev) {
        qc.setQueryData(
          queryKeys.analyses(projectId),
          ctx.prev
        );
      }
    },

    onSuccess: () => {
      qc.invalidateQueries({
        queryKey: queryKeys.analyses(projectId),
      });
    },
  });
}