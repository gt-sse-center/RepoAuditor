# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireSignedCommits object."""

from RepoAuditor.Plugins.GitHubRulesets.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireSignedCommits(EnableRulesetRequirementImpl):
    """Require signed commits."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireSignedCommits",
            default_value=False,
            dynamic_arg_name="true",
            github_ruleset_type="Signed Commits",
            github_ruleset_value="required_signatures",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "required_signatures",
            resolution="Enable commit signing requirement in repository rulesets",
            rationale="Signed commits ensure commit authenticity",
        )
