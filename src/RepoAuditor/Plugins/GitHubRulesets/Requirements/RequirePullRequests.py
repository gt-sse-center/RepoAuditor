# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequirePullRequests object."""

from RepoAuditor.Plugins.GitHubRulesets.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequirePullRequests(EnableRulesetRequirementImpl):
    """Require pull requests before merging to default branch."""

    def __init__(self) -> None:
        super().__init__(
            name="RequirePullRequests",
            default_value=False,
            dynamic_arg_name="true",
            github_ruleset_type="Pull Requests",
            github_ruleset_value="pull_request",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "pull_request",
            resolution="Enable pull request requirements in repository rulesets",
            rationale="Pull request reviews help maintain code quality and collaboration",
        )
