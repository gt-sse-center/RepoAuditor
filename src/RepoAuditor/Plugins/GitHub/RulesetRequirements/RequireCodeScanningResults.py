# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireCodeScanningResultsRule requirement."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireCodeScanningResultsRule(EnableRulesetRequirementImpl):
    """Requirement which checks for the ruleset rule regarding code scanning results."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireCodeScanningResultsRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="code_scanning",
            github_ruleset_value="Require code scanning results",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to enable requiring the results of code scanning.

                Reasons for this Default
                ------------------------
                - Code scanning can help prevent security vulnerabilities and errors in your code.

                Reasons to Override this Default
                --------------------------------
                - Different users/organization may have different tools for scanning code for security vulnerabilities.
                - Single-user repositories that don't use secrets may not need this feature.
                """
            ),
        )
