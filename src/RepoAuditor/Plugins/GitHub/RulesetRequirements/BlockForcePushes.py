# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the BlockForcePushesRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class BlockForcePushesRule(EnableRulesetRequirementImpl):
    """Requirement for rule to block force pushes to the matching branch."""

    def __init__(self) -> None:
        super().__init__(
            name="BlockForcePushesRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="non_fast_forward",
            github_ruleset_value="Block force pushes to the specified branch",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "non_fast_forward",
            resolution="{__enabled_str} rule in the repository rulesets which blocks force pushes to the 'main' branch",
            rationale="Blocking force pushes to the 'main' branch can ensure proper code review and quality.",
        )
