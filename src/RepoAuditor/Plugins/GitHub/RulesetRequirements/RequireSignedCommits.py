# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireSignedCommits object."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireSignedCommits(EnableRulesetRequirementImpl):
    """Check that the "Require signed commits" rule is disabled."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireSignedCommitsRule",
            enabled_by_default=True,
            dynamic_arg_name="disabled",
            github_ruleset_type="required_signatures",
            github_ruleset_value="Require signed commits",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "required_signatures",
            resolution="{__enabled_str} commit signing requirement in repository rulesets",
            rationale="Signed commits ensure commit authenticity",
        )
