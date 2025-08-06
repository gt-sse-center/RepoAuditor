# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RestrictCreationsRule requirement."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RestrictCreationsRule(EnableRulesetRequirementImpl):
    """Restrict creation of branches or tags which match specified patterns."""

    def __init__(self) -> None:
        super().__init__(
            name="RestrictCreationsRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="creation",
            github_ruleset_value="Restrict creations",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to disable unauthorized creation of the primary branch.

                Reasons for this Default
                ------------------------
                - Disables accidental creation of matching refs/branches, which can help prevent code divergence.

                Reasons to Override this Default
                --------------------------------
                - A user with git expertise wants to create a matching branch for a specific reason.
                """,
            ),
        )
