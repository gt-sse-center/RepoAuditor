# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireSuccessfulDeploymentsRule requirement."""

import textwrap

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
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to not require successful deployments to specific environments.
                Adds a layer of checks which are required before the primary development branch
                can be updated.

                Reasons for this Default
                ------------------------
                - Configuring deployment environments is non-trivial and requires some dev-ops expertise,
                  which isn't always needed depending on the project.

                Reasons to Override this Default
                --------------------------------
                - Your code is required to run on specific environments and settings,
                  which can be configured.
                """,
            ),
        )
