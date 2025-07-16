# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequirePullRequests object."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequirePullRequests(EnableRulesetRequirementImpl):
    """Require pull requests before merging to default branch."""

    def __init__(self) -> None:
        super().__init__(
            name="RequirePullRequestsRule",
            enabled_by_default=True,
            dynamic_arg_name="disabled",
            github_ruleset_type="pull_request",
            github_ruleset_value="Require a pull request before merging",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "pull_request",
            resolution="{__enabled_str} pull request rule in repository rulesets",
            rationale="Pull request reviews help maintain code quality and collaboration",
        )
