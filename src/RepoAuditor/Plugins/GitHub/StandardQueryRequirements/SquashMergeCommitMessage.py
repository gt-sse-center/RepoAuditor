# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SquashMergeCommitMessage object"""

import textwrap

from typing import Any

from ..Impl.ValueRequirementImpl import DoesNotApplyResult, ValueRequirementImpl


# ----------------------------------------------------------------------
class SquashMergeCommitMessage(ValueRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SquashMergeCommitMessage, self).__init__(
            "SquashMergeCommitMessage",
            "COMMIT_MESSAGES",
            "settings",
            "Pull Requests",
            "Allow squash merging -> Default...",
            _GetValue,
            textwrap.dedent(
                """\
                Available values:

                BLANK [Default to pull request title]
                    Pull Request title and number on the first line.

                COMMIT_MESSAGES [Default to pull request title and commit details]
                    Commit title and...
                        [Single Commit] ...commit message
                        [Multiple Commits] ...pull request title and number and list of commits

                PR_BODY [Default to pull request title and description]
                    Pull Request title and number on the first line; commit description starting on the third line.

            The default setting is COMMIT_MESSAGES.

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
