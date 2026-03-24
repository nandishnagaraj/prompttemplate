export interface BitbucketPullRequestRef {
  commit?: {
    hash?: string;
  };
}

export interface BitbucketPullRequest {
  id: number;
  title?: string;
  description?: string;
  source?: BitbucketPullRequestRef;
  links?: {
    html?: {
      href?: string;
    };
  };
}

export interface BitbucketRepository {
  slug?: string;
  name?: string;
  full_name?: string;
  workspace?: {
    slug?: string;
  };
}

export interface BitbucketWebhookPayload {
  pullrequest?: BitbucketPullRequest;
  repository?: BitbucketRepository;
  eventKey?: string;
}

export type ReviewVerdict = "pass" | "warn" | "fail";
export type ReviewSeverity = "blocker" | "warning" | "suggestion";
export type ReviewCategory = "security" | "correctness" | "maintainability" | "tests" | "api";

export interface ReviewFinding {
  severity: ReviewSeverity;
  category: ReviewCategory;
  title: string;
  detail: string;
  filePath: string;
  line: number;
  confidence?: number;
}

export interface ReviewSummary {
  verdict: ReviewVerdict;
  headline: string;
  overview: string;
}

export interface ReviewResponse {
  summary: ReviewSummary;
  findings: ReviewFinding[];
}
