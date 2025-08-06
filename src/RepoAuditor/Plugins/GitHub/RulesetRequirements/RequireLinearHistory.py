# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireLinearHistoryRule requirement."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequireLinearHistoryRule(EnableRulesetRequirementImpl):
    """Requirement for setting which prevents merge commits to specified pattern in the rule."""

    def __init__(self) -> None:
        super().__init__(
            name="RequireLinearHistoryRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="required_linear_history",
            github_ruleset_value="Require linear history",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to not require a linear history as this option is disabled when rebase
                merging and squash merging are disabled (which are the default validation settings).

                Reasons for this Default
                ------------------------
                - This option is disabled within the GitHub UX when rebase merging and squash merging are disabled
                  (which are the default validation settings).

                Reasons to Override this Default
                --------------------------------
                - You have enabled rebase merging or squash merging
                """,
            ),
        )
