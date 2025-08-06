# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RestrictUpdatesRule requirement."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RestrictUpdatesRule(EnableRulesetRequirementImpl):
    """Restrict updates of branches or tags which match specified patterns."""

    def __init__(self) -> None:
        super().__init__(
            name="RestrictUpdatesRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="update",
            github_ruleset_value="Restrict updates",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to disable unauthorized updates to the primary branch.

                Reasons for this Default
                ------------------------
                - Disables accidental updates of matching refs/branches, which can help prevent code divergence.

                Reasons to Override this Default
                --------------------------------
                - A user with git expertise wants to update a matching branch for a specific reason.
                """,
            ),
        )
