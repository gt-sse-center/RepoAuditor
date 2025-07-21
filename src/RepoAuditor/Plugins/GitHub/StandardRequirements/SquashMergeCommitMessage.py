# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SquashMergeCommitMessage object."""

import textwrap
from typing import Any

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardValueRequirementImpl import (
    DoesNotApplyResult,
    StandardValueRequirementImpl,
)


# ----------------------------------------------------------------------
class SquashMergeCommitMessage(StandardValueRequirementImpl):
    """Set default commit message for squash merges."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "SquashMergeCommitMessage",
            "COMMIT_MESSAGES",
            "settings",
            "Pull Requests",
            "Allow squash merging -> Default...",
            _GetValue,
            textwrap.dedent(
                """\
                Available values on GitHub:

                Default to pull request title [BLANK]
                    Pull Request title and number on the first line.

                Default to pull request title and commit details [COMMIT_MESSAGES]
                    Commit title and...
                        [Single Commit] ...commit message
                        [Multiple Commits] ...pull request title and number and list of commits

                Default to pull request title and description [PR_BODY]
                    Pull Request title and number on the first line; commit description starting on the third line.

            The default setting is "Default to pull request title and commit details [COMMIT_MESSAGES]".

            Reasons for this Default
            ------------------------
            - Preserves the information in the original commits.

            Reasons to Override this Default
            --------------------------------
            <unknown>
            """,
            ),
        )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(data: dict[str, Any]) -> str | DoesNotApplyResult | None:
    data = data["standard"]

    result = data.get("allow_squash_merge", None)
    if result is None:
        return None

    if not result:
        return DoesNotApplyResult("Squash merge commits are not enabled.")

    return data.get("squash_merge_commit_message", None)
