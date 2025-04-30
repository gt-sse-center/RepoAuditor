# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireStatusChecks object."""

from typing import override, Any
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class RequireStatusChecks(Requirement):
    """Implement the Status Check ruleset for a branch."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireStatusChecks",
            description="Require status checks to pass before merging",
            style=ExecutionStyle.Parallel,
            resolution_template="Configure required status checks in repository rulesets",
            rationale_template="Status checks ensure code quality and compatibility",
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
                and len(ruleset.get("parameters", {}).get("required_status_checks", [])) > 0
            ):
                return self.EvaluateImplResult(
                    EvaluateResult.Success, f"Ruleset '{ruleset['name']}' enforces status checks"
                )

        return self.EvaluateImplResult(
            EvaluateResult.Error,
            "No active branch ruleset requiring status checks found",
            provide_resolution=True,
        )
