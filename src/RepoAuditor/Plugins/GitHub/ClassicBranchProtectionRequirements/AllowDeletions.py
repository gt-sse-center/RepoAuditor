# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the AllowDeletions object."""

import textwrap

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicEnableRequirementImpl import (
    ClassicEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class AllowDeletions(ClassicEnableRequirementImpl):
    """Allow deletion of the mainline branch."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "AllowDeletions",
            False,
            "enabled",
            "Rules applied to everyone including administrators",
            "Allow deletions",
            lambda data: data["branch_protection_data"]["allow_deletions"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to not allow the deletion of the mainline branch.

                Reasons for this Default
                ------------------------
                - Bad things happen when the mainline branch is deleted.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
