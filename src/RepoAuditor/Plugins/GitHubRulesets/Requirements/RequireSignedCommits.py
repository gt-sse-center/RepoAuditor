# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireSignedCommits object."""

from typing import override, Any
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class RequireSignedCommits(Requirement):
    """Implement the Signed Commits required ruleset for a branch."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireSignedCommits",
            description="Require signed commits",
            style=ExecutionStyle.Parallel,
            resolution_template="Enable commit signing requirement in repository rulesets",
            rationale_template="Signed commits ensure commit authenticity",
        )

    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        rulesets = query_data.get("rulesets", [])

        for ruleset in rulesets:
            if (
                ruleset.get("enforcement", "") == "active"
                and ruleset.get("target", "") == "branch"
                and ruleset.get("parameters", {}).get("commit_signatures", False)
            ):
                return self.EvaluateImplResult(
                    EvaluateResult.Success, f"Ruleset '{ruleset['name']}' enforces signed commits"
                )

        return self.EvaluateImplResult(
            EvaluateResult.Error,
            "No active branch ruleset requiring signed commits found",
            provide_resolution=True,
        )
