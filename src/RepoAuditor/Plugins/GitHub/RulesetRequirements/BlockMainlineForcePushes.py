# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the BlockMainlineForcePushesRule requirement."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class BlockMainlineForcePushesRule(EnableRulesetRequirementImpl):
    """Requirement for rule to block force pushes to the mainline branch."""

    def __init__(self) -> None:
        super().__init__(
            name="BlockMainlineForcePushesRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="non_fast_forward",
            github_ruleset_value="Block force pushes",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to not allow force pushes to the mainline branch.

                Reasons for this Default
                ------------------------
                - Force pushes rewrite history, which breaks git lineage for all other clones of the repository.
                  Merges are possible when this happens, but they are difficult to perform and data loss is
                  possible.

                Reasons to Override this Default
                --------------------------------
                - If the repository only has a single developer or if is private.
                """,
            ),
        )
