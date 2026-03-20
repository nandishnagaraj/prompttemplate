import "dotenv/config";
import crypto from "node:crypto";
import express, { type Request, type Response } from "express";
import {
  createCommitStatus,
  createInlinePullRequestComment,
  createPullRequestComment,
  getPullRequest,
  getPullRequestDiff
} from "./bitbucket.js";
import { dedupeFindings } from "./dedupe.js";
import { reviewWithGemini } from "./gemini.js";
import { buildReviewPrompt } from "./prompt.js";
import type { BitbucketWebhookPayload, ReviewFinding, ReviewResponse, ReviewVerdict } from "./types.js";

const app = express();
app.use(express.json({ limit: "2mb" }));

const PORT = Number(process.env.PORT ?? 3000);
const BOT_TAG = process.env.BOT_TAG ?? "ai-review-bot";
const MAX_DIFF_CHARS = Number(process.env.MAX_DIFF_CHARS ?? 120000);
const POST_SUMMARY_COMMENT = toBoolean(process.env.POST_SUMMARY_COMMENT, true);
const POST_INLINE_COMMENTS = toBoolean(process.env.POST_INLINE_COMMENTS, false);
const POST_BUILD_STATUS = toBoolean(process.env.POST_BUILD_STATUS, false);
const MIN_INLINE_CONFIDENCE = Number(process.env.MIN_INLINE_CONFIDENCE ?? 0.8);

app.get("/health", (_req: Request, res: Response) => {
  res.json({ ok: true });
});

app.post("/webhook/bitbucket", async (req: Request<unknown, unknown, BitbucketWebhookPayload>, res: Response) => {
  try {
    if (!verifyWebhook(req)) {
      return res.status(401).json({ ok: false, error: "Invalid webhook signature" });
    }

    if (!isPullRequestEvent(req)) {
      return res.status(200).json({ ok: true, skipped: true, reason: "Not a PR event" });
    }

    const { workspace, repoSlug, prId } = parseRepoInfo(req.body);
    const result = await runReview({ workspace, repoSlug, prId });
    return res.status(200).json({ ok: true, result });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Internal error";
    console.error("Webhook error:", error);
    return res.status(500).json({ ok: false, error: message });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

function toBoolean(value: string | undefined, defaultValue: boolean): boolean {
  if (value === undefined) {
    return defaultValue;
  }
  return value.toLowerCase() === "true";
}

function safeEqual(a: string, b: string): boolean {
  const bufferA = Buffer.from(a);
  const bufferB = Buffer.from(b);
  if (bufferA.length !== bufferB.length) {
    return false;
  }
  return crypto.timingSafeEqual(bufferA, bufferB);
}

function verifyWebhook(req: Request<unknown, unknown, BitbucketWebhookPayload>): boolean {
  const secret = process.env.BITBUCKET_WEBHOOK_SECRET;
  if (!secret) {
    return true;
  }

  const header =
    req.header("x-hub-signature") ??
    req.header("x-hub-signature-256") ??
    req.header("x-bb-signature");

  if (!header) {
    return false;
  }

  const rawBody = JSON.stringify(req.body);
  const hmac = crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
  const normalizedHeader = header.replace(/^sha256=/, "");
  return safeEqual(normalizedHeader, hmac);
}

function isPullRequestEvent(req: Request<unknown, unknown, BitbucketWebhookPayload>): boolean {
  const eventKey = req.header("x-event-key") ?? req.body.eventKey ?? "";
  return ["pullrequest:created", "pullrequest:updated"].includes(eventKey);
}

function parseRepoInfo(payload: BitbucketWebhookPayload): { workspace: string; repoSlug: string; prId: number } {
  const workspace = payload.repository?.workspace?.slug ?? payload.repository?.full_name?.split("/")[0];
  const repoSlug = payload.repository?.slug ?? payload.repository?.name;
  const prId = payload.pullrequest?.id;

  if (!workspace || !repoSlug || !prId) {
    throw new Error("Could not determine workspace, repo slug, or PR id from webhook payload");
  }

  return { workspace, repoSlug, prId };
}

function truncateDiff(diffText: string): string {
  if (diffText.length <= MAX_DIFF_CHARS) {
    return diffText;
  }
  return `${diffText.slice(0, MAX_DIFF_CHARS)}\n\n[TRUNCATED]`;
}

function mapVerdictToBuildState(verdict: ReviewVerdict): "SUCCESSFUL" | "FAILED" {
  return verdict === "fail" ? "FAILED" : "SUCCESSFUL";
}

function renderSummaryComment(prId: number, commitHash: string | undefined, review: ReviewResponse): string {
  const blockers = review.findings.filter((finding) => finding.severity === "blocker");
  const warnings = review.findings.filter((finding) => finding.severity === "warning");
  const suggestions = review.findings.filter((finding) => finding.severity === "suggestion");

  const lines: string[] = [];
  lines.push(`<!-- ${BOT_TAG}:${prId}:${commitHash ?? "unknown"} -->`);
  lines.push("## AI Code Review");
  lines.push(`**Verdict:** ${review.summary.verdict.toUpperCase()}`);
  lines.push(`**Headline:** ${review.summary.headline}`);
  lines.push("");
  lines.push(review.summary.overview);
  lines.push("");

  appendFindings(lines, "Blockers", blockers);
  appendFindings(lines, "Warnings", warnings);
  appendFindings(lines, "Suggestions", suggestions);

  if (review.findings.length === 0) {
    lines.push("No actionable issues found in the submitted diff.");
    lines.push("");
  }

  lines.push(`_Generated automatically by ${BOT_TAG}_`);
  return lines.join("\n");
}

function appendFindings(lines: string[], heading: string, findings: ReviewFinding[]): void {
  if (findings.length === 0) {
    return;
  }

  lines.push(`### ${heading}`);
  findings.slice(0, 10).forEach((finding, index) => {
    lines.push(`${index + 1}. **${finding.title}** — \`${finding.filePath}:${finding.line}\`  `);
    lines.push(finding.detail);
  });
  lines.push("");
}

function renderInlineComment(finding: ReviewFinding): string {
  return [
    `**${finding.severity.toUpperCase()}: ${finding.title}**`,
    "",
    finding.detail,
    "",
    `Category: ${finding.category} | Confidence: ${finding.confidence ?? "n/a"}`
  ].join("\n");
}

async function runReview(input: { workspace: string; repoSlug: string; prId: number }): Promise<Record<string, unknown>> {
  const pr = await getPullRequest(input.workspace, input.repoSlug, input.prId);
  const rawDiff = await getPullRequestDiff(input.workspace, input.repoSlug, input.prId);
  const diffText = truncateDiff(rawDiff);

  const prompt = buildReviewPrompt({
    pr: {
      title: pr.title,
      description: pr.description
    },
    diffText
  });

  const review = await reviewWithGemini({ prompt });

  review.findings = dedupeFindings(review.findings);

  if (POST_SUMMARY_COMMENT) {
    const body = renderSummaryComment(pr.id, pr.source?.commit?.hash, review);
    await createPullRequestComment(input.workspace, input.repoSlug, input.prId, body);
  }

  if (POST_INLINE_COMMENTS) {
    for (const finding of review.findings) {
      if ((finding.confidence ?? 0) < MIN_INLINE_CONFIDENCE) {
        continue;
      }

      try {
        await createInlinePullRequestComment(
          input.workspace,
          input.repoSlug,
          input.prId,
          renderInlineComment(finding),
          finding.filePath,
          finding.line
        );
      } catch (error) {
        console.warn("Inline comment failed", {
          filePath: finding.filePath,
          line: finding.line,
          error
        });
      }
    }
  }

  if (POST_BUILD_STATUS && pr.source?.commit?.hash) {
    await createCommitStatus(
      input.workspace,
      input.repoSlug,
      pr.source.commit.hash,
      mapVerdictToBuildState(review.summary.verdict),
      "ai-code-review",
      "AI Code Review",
      review.summary.headline,
      pr.links?.html?.href
    );
  }

  return {
    workspace: input.workspace,
    repoSlug: input.repoSlug,
    prId: input.prId,
    reviewedCommit: pr.source?.commit?.hash ?? null,
    verdict: review.summary.verdict,
    findingCount: review.findings.length
  };
}
