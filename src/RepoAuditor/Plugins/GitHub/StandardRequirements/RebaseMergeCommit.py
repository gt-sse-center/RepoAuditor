# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RebaseMergeCommit object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class RebaseMergeCommit(StandardEnableRequirementImpl):
    """Allow rebase merging requirement."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "RebaseMergeCommit",
            False,
            "enabled",
            "settings",
            "Pull Requests",
            "Allow rebase merging",
            lambda data: data["standard"].get("allow_rebase_merge", None),
            textwrap.dedent(
                """\
                The default behavior is to not allow rebase merging.

                Reasons for this Default
                ------------------------
                - Rebase merging is not compatible with signed commits, as GitHub creates a new commit when rebasing.

                Reasons to Override this Default
                --------------------------------
                - Your repository does not require signatures.
                - You want GitHub to rebase for you as part of the pull request process when changes by others are frequent or the
                  pull request process can last for an extended period of time.
                """,
            ),
        )
