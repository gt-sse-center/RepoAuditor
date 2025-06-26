# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireStatusChecks object."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireStatusChecks(EnableRulesetRequirementImpl):
    """Require status checks to pass before merging."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireStatusChecks",
            enabled_by_default=False,
            dynamic_arg_name="enabled",
            github_ruleset_type="required_status_checks",
            github_ruleset_value="Status Checks",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "required_status_checks",
            resolution="Configure required status checks in repository rulesets",
            rationale="Status checks ensure code quality and compatibility",
        )
