# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SuggestUpdatingPullRequestBranches object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class SuggestUpdatingPullRequestBranches(StandardEnableRequirementImpl):
    """Always suggest updating pull request branches."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "SuggestUpdatingPullRequestBranches",
            False,
            "enabled",
            "settings",
            "Pull Requests",
            "Always suggest updating pull request branches",
            lambda data: data["standard"].get("allow_update_branch", None),
            textwrap.dedent(
                """\
                The default behavior is to not suggest updating branches associated with pull requests within the pull request.

                Reasons for this Default
                ------------------------
                - Pull requests updated by GitHub are not compatible with signed commits, as GitHub creates a new commit when rebasing.
                - Rebasing may introduce changes that are incompatible with the current pull request.

                Reasons to Override this Default
                --------------------------------
                - Your repository does not require signatures.
                - Merge problems more insidious than conflicts are infrequent.
                """,
            ),
        )
