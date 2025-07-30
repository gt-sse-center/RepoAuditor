# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireStatusChecksToPassRule object."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireStatusChecksToPassRule(EnableRulesetRequirementImpl):
    """Require status checks to pass before merging."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireStatusChecksToPassRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="required_status_checks",
            github_ruleset_value="Require status checks to pass",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to require status checks to pass before merging a pull request.

                Reasons for this Default
                ------------------------
                - Status checks are an important part of the development process and should not be bypassed.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
