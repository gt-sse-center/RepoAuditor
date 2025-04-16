from typing import override
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement

class RequireStatusChecks(Requirement):
    def __init__(self):
        super().__init__(
            name="RequireStatusChecks",
            description="Require status checks to pass before merging",
            style=ExecutionStyle.Parallel,
            resolution_template="Configure required status checks in repository rulesets",
            rationale_template="Status checks ensure code quality and compatibility",
        )

    @override
    def _EvaluateImpl(self, query_data, requirement_args):
        rulesets = query_data.get("rulesets", [])
        
        for ruleset in rulesets:
            if ruleset.get("enforcement", "") == "active" and \
               ruleset.get("target", "") == "branch" and \
               len(ruleset.get("parameters", {}).get("required_status_checks", [])) > 0:
                return self.EvaluateImplResult(
                    EvaluateResult.Success,
                    f"Ruleset '{ruleset['name']}' enforces status checks"
                )

        return self.EvaluateImplResult(
            EvaluateResult.Error,
            "No active branch ruleset requiring status checks found",
            provide_resolution=True
        )