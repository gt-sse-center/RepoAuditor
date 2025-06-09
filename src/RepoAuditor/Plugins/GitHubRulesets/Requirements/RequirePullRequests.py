# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequirePullRequests object."""

from typing import override, Any
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class RequirePullRequests(Requirement):
    """Implement the Pull Requests required ruleset for the branch."""

    def __init__(self) -> None:
        super().__init__(
            name="RequirePullRequests",
            description="Require pull requests before merging to default branch",
            style=ExecutionStyle.Parallel,
            resolution_template="Enable pull request requirements in repository rulesets",
            rationale_template="Pull request reviews help maintain code quality and collaboration",
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
                and ruleset.get("parameters", {}).get("pull_request", {}).get("required", False)
            ):
                return self.EvaluateImplResult(
                    EvaluateResult.Success, f"Ruleset '{ruleset['name']}' enforces pull requests"
                )

        return self.EvaluateImplResult(
            EvaluateResult.Error,
            "No active branch ruleset requiring pull requests found",
            provide_resolution=True,
        )
