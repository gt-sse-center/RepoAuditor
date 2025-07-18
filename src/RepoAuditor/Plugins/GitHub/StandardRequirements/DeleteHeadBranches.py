# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the DeleteHeadBranches object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class DeleteHeadBranches(StandardEnableRequirementImpl):
    """Requirement to delete head branches."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "DeleteHeadBranches",
            True,
            "disabled",
            "settings",
            "Pull Requests",
            "Automatically delete head branches",
            lambda data: data["standard"].get("delete_branch_on_merge", None),
            textwrap.dedent(
                """\
                The default behavior is to automatically delete head branches once they have been merged into the mainline branch.

                Reasons for this Default
                ------------------------
                - Long-lived branches make integration more difficult due to changes that accumulate over time.

                Reasons to Override this Default
                --------------------------------
                - You support release branches and may want to merge changes from this release branch into the mainline branch
                  (although, it is possible to workaround this issue by creating a pull request from a temporary branch that
                  includes cherry-picked changes from the release branch).
                """,
            ),
        )
