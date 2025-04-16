from typing import override
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement

class RequirePullRequests(Requirement):
    def __init__(self):
        super().__init__(
            name="RequirePullRequests",
            description="Require pull requests before merging to default branch",
            style=ExecutionStyle.Parallel,
            resolution_template="Enable pull request requirements in repository rulesets",
            rationale_template="Pull request reviews help maintain code quality and collaboration",
        )

    @override
    # 以RequirePullRequests为例

    def _EvaluateImpl(self, query_data, requirement_args):
     rulesets = query_data.get("rulesets", [])
    
     for ruleset in rulesets:
        if ruleset.get("enforcement") == "active" and \
           ruleset.get("target") == "branch" and \
           ruleset.get("rules", {}).get("pull_request", {}).get("required"):
            return self.EvaluateImplResult(
                EvaluateResult.Success,
                f"ruleset'{ruleset['name']}' check"
            )
    
     return self.EvaluateImplResult(
        EvaluateResult.Error,
        "No Find Rule",
        provide_resolution=True
    )
