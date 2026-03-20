from __future__ import annotations

import os
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PromptLibrary:
    """Loads prompt templates from the bundled prompt-library folder."""

    def __init__(self, root: str):
        self.root = Path(root)

    def load(self, rel_path: str) -> str:
        p = self.root / rel_path
        if not p.exists():
            raise FileNotFoundError(f"Prompt not found: {p}")
        return read_text(p)

    # Convenience accessors (paths match the original library structure)
    def prd_full(self) -> str:
        return self.load("01-prd/PRD-02-full-prd-generation.md")

    def prd_gap(self) -> str:
        return self.load("01-prd/PRD-03-gap-analysis-validation.md")

    def prd_rtm(self) -> str:
        return self.load("01-prd/PRD-04-traceability-matrix.md")

    def stories_from_prd(self) -> str:
        return self.load("02-user-stories/US-01-story-generation-from-prd.md")

    def architecture_design(self) -> str:
        return self.load("03-design/DES-01-architecture-design.md")

    def openapi_contract(self) -> str:
        return self.load("03-design/DES-03-openapi-contract.md")

    def arch_risk_review(self) -> str:
        return self.load("03-design/DES-04-architecture-risk-review.md")

    def dev_implementation(self) -> str:
        return self.load("04-development/DEV-01-feature-implementation.md")

    def test_plan_unit(self) -> str:
        return self.load("05-testing/TEST-01-unit-test-generation.md")

    def test_plan_integration(self) -> str:
        return self.load("05-testing/TEST-02-integration-test-generation.md")

    def test_security(self) -> str:
        return self.load("05-testing/TEST-04-security-test-cases.md")

    def test_coverage_gaps(self) -> str:
        return self.load("05-testing/TEST-03-coverage-gap-analysis.md")
