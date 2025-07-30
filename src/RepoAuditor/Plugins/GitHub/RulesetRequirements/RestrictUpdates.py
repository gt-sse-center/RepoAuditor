# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RestrictUpdatesRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RestrictUpdatesRule(EnableRulesetRequirementImpl):
    """Restrict updates of branches or tags which match specified patterns."""

    def __init__(self) -> None:
        super().__init__(
            name="RestrictUpdatesRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="update",
            github_ruleset_value="Restrict updates to the branch",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "update",
            resolution="{__enabled_str} rule in the repository rulesets to restrict updates of the 'main' branch",
            rationale="Prevents unauthorized updates of the 'main' branch.",
        )
