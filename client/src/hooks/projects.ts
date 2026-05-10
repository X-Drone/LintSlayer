import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { queryKeys, request } from "./api";
import type { CreateProjectRequest, CreateProjectResponse, GetProjectResponse, GetProjectsResponse } from "./types";

// GET /projects/
export function useProjects() {
  return useQuery({
    queryKey: queryKeys.projects,
    queryFn: () => request<GetProjectsResponse>("/projects/"),
  });
}

export function useProject(projectId: number) {
  return useQuery({
    queryKey: queryKeys.project(projectId),
    queryFn: () =>
      request<GetProjectResponse>(`/projects/${projectId}`),
    enabled: !!projectId,
  });
}

export function useCreateProject() {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateProjectRequest) =>
      request<CreateProjectResponse>("/projects/create", {
        method: "POST",
        body: JSON.stringify(data),
      }),

    onSuccess: () => {
      qc.invalidateQueries({ queryKey: queryKeys.projects });
    },
  });
}

export function useDeleteProject() {
  const qc = useQueryClient();

  return useMutation({
    mutationFn: (projectId: number) =>
      request(`/projects/${projectId}`, {
        method: "DELETE",
      }),

    onSuccess: (_, projectId) => {
      qc.invalidateQueries({ queryKey: queryKeys.projects });
      qc.removeQueries({ queryKey: queryKeys.project(projectId) });
    },
  });
}
