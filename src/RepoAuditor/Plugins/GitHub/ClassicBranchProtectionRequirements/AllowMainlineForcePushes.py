# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the AllowMainlineForcePushes object."""

import textwrap

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicEnableRequirementImpl import (
    ClassicEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class AllowMainlineForcePushes(ClassicEnableRequirementImpl):
    """Allow force pushes to the mainline branch."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "AllowMainlineForcePushes",
            False,
            "enabled",
            "Rules applied to everyone including administrators",
            "Allow force pushes",
            lambda data: data["branch_protection_data"]["allow_force_pushes"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to not allow force pushes to the mainline branch.

                Reasons for this Default
                ------------------------
                - Force pushes rewrite history, which breaks git lineage for all other clones of the repository.
                  Merges are possible when this happens, but they are difficult to perform and data loss is
                  possible.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
