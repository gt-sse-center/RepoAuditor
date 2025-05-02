from typing import override
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class RequireSignedCommits(Requirement):
    def __init__(self):
        super().__init__(
            name="RequireSignedCommits",
            description="Require signed commits",
            style=ExecutionStyle.Parallel,
            resolution_template="Enable commit signing requirement in repository rulesets",
            rationale_template="Signed commits ensure commit authenticity",
        )

    @override
    def _EvaluateImpl(self, query_data, requirement_args):
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
