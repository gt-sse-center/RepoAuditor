# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RestrictCreationsRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RestrictCreationsRule(EnableRulesetRequirementImpl):
    """Restrict creation of branches or tags which match specified patterns."""

    def __init__(self) -> None:
        super().__init__(
            name="RestrictCreationsRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="creation",
            github_ruleset_value="Restrict creation of the branch",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "creation",
            resolution="{__enabled_str} rule in the repository rulesets to restrict creation of a 'main' branch",
            rationale="Prevents unauthorized creation of 'main' branch.",
        )
