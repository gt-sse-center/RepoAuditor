# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SquashCommitMerge object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class SquashCommitMerge(StandardEnableRequirementImpl):
    """Allow squash merging."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "SquashCommitMerge",
            False,
            "enabled",
            "settings",
            "Pull Requests",
            "Allow squash merging",
            lambda data: data["standard"].get("allow_squash_merge", None),
            textwrap.dedent(
                """\
                The default behavior is to not allow squash merging.

                Reasons for this Default
                ------------------------
                - When performing a Squash & Merge, GitHub creates a new merge commit with its key.
                This makes it difficult to verify author signatures when looking at the commit history.

                Reasons to Override this Default
                --------------------------------
                - Your repository does not require signatures.
                - You want to ensure that single-commit-changes are merged into the mainline branch to simplify the branch's history.
                """,
            ),
        )
