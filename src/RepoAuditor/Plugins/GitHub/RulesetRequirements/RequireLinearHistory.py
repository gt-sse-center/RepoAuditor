# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireLinearHistoryRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireLinearHistoryRule(EnableRulesetRequirementImpl):
    """Requirement for setting which prevents merge commits to specified pattern in the rule."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireLinearHistoryRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="required_linear_history",
            github_ruleset_value="Prevent merge commits on branch",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "required_linear_history",
            resolution="{__enabled_str} rule to prevent merge commits to 'main' branch in repository rulesets",
            rationale="Prevention of merge commits helps maintain a linear commit history, making it easier to navigate commits.",
        )
