export type Nullable<T> = T | null;


export interface ProjectsResponse {
  names: string[];
}

export interface ProjectCreateRequest {
  name: string;
  repo_url?: Nullable<string>;
  ext?: Nullable<string>;
  content?: Nullable<string>;
}

export interface ProjectResponse {
  id: number;
  name: string;
  owner: string;
  files: string[];
}

export type ProjectDetailResponse = ProjectResponse;


export const AnalysisStatus = {
  Pending: "pending",
  Running: "running",
  Completed: "completed",
  Failed: "failed",
} as const;

export type AnalysisStatus =
  typeof AnalysisStatus[keyof typeof AnalysisStatus];

export interface AnalysisRunResponse {
  id: number;
  project_id: number;
  status: AnalysisStatus;
  timestamp: Nullable<string>;
}

export interface AnalysisDetailResponse extends AnalysisRunResponse {
  issues: IssueResponse[];
}

export const IssueSeverity = {
  Low: "low",
  Medium: "medium",
  High: "high",
  Critical: "critical",
} as const;

export type IssueSeverity =
  typeof IssueSeverity[keyof typeof IssueSeverity];

export interface IssueResponse {
  id: number;
  file_path: string;
  line_start: number;
  line_end: number;
  severity: IssueSeverity;
  message: string;
}


export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}


export type GetProjectsResponse = ProjectsResponse;

export type CreateProjectRequest = ProjectCreateRequest;
export type CreateProjectResponse = ProjectResponse;

export type GetProjectResponse = ProjectDetailResponse;

export type RunAnalyseRequest = string[]; // список анализаторов
export type RunAnalyseResponse = AnalysisRunResponse;

export type GetAnalysesResponse = AnalysisRunResponse[];
export type GetAnalyseResponse = AnalysisDetailResponse;
