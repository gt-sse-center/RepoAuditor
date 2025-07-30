# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireSuccessfulDeploymentsRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireSuccessfulDeploymentsRule(EnableRulesetRequirementImpl):
    """Requirement for rule requiring successful deployments to the matching branch in the ruleset."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireSuccessfulDeploymentsRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="required_deployments",
            github_ruleset_value="Require deployments to succeed",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "required_deployments",
            resolution="{__enabled_str} rule in the repository rulesets which requires deployments to the 'main' branch to succeed",
            rationale="Adds a layer of checks which are required before the 'main' branch can be updated.",
        )
