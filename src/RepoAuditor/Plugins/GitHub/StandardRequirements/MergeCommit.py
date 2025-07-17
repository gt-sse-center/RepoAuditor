# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the MergeCommit object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class MergeCommit(StandardEnableRequirementImpl):
    """Allow merge commits requirement."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "MergeCommit",
            True,
            "disabled",
            "settings",
            "Pull Requests",
            "Allow merge commits",
            lambda data: data["standard"].get("allow_merge_commit", None),
            textwrap.dedent(
                """\
                The default behavior is to allow merge commits.

                Reasons for this Default
                ------------------------
                - Merge commits are the most basic way to merge from a branch into another branch.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
