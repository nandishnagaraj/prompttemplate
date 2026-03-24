import type { ReviewFinding } from "./types.js";

export function fingerprintFinding(finding: ReviewFinding): string {
  return [
    finding.severity,
    finding.category,
    finding.title,
    finding.filePath,
    String(finding.line)
  ].join("|");
}

export function dedupeFindings(findings: ReviewFinding[]): ReviewFinding[] {
  const seen = new Set<string>();
  const result: ReviewFinding[] = [];

  for (const finding of findings) {
    if (!finding.filePath || !finding.line || !finding.title) {
      continue;
    }

    const fingerprint = fingerprintFinding(finding);
    if (seen.has(fingerprint)) {
      continue;
    }

    seen.add(fingerprint);
    result.push(finding);
  }

  const severityOrder: Record<ReviewFinding["severity"], number> = {
    blocker: 0,
    warning: 1,
    suggestion: 2
  };

  return result.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);
}
