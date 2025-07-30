# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RestrictDeletionsRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RestrictDeletionsRule(EnableRulesetRequirementImpl):
    """Restrict deletion of branches or tags which match specified rule patterns."""

    def __init__(self) -> None:
        super().__init__(
            name="RestrictDeletionsRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="deletions",
            github_ruleset_value="Restrict deletion of the branch",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "deletions",
            resolution="{__enabled_str} rule in the repository rulesets to restrict deletion of the 'main' branch",
            rationale="Prevents unauthorized deletion of the 'main' branch.",
        )
