# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireCodeScanningResultsRule requirement."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireCodeScanningResultsRule(EnableRulesetRequirementImpl):
    """Requirement which checks for the ruleset rule regarding code scanning results."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireCodeScanningResultsRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="code_scanning",
            github_ruleset_value="Require code scanning results",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "code_scanning",
            resolution="{__enabled_str} rule in the repository ruleset which requires results from code scanning tools",
            rationale="Code scanning can help prevent security vulnerabilities and errors in your code.",
        )
