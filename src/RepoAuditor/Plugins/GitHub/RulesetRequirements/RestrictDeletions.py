# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RestrictDeletionsRule requirement."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RestrictDeletionsRule(EnableRulesetRequirementImpl):
    """Restrict deletion of branches or tags which match specified rule patterns."""

    def __init__(self) -> None:
        super().__init__(
            name="RestrictDeletionsRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="deletions",
            github_ruleset_value="Restrict deletions",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to disable unauthorized deletion of the primary branch.

                Reasons for this Default
                ------------------------
                - Disables accidental deletion of matching refs/branches, which can help safeguard the code.

                Reasons to Override this Default
                --------------------------------
                - A user with git expertise wants to delete the matching branch for a specific reason.
                """,
            ),
        )
