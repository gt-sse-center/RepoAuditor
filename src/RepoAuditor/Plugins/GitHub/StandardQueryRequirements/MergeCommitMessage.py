# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the MergeCommitMessage object"""

import textwrap

from typing import Any

from .Impl.StandardValueRequirementImpl import DoesNotApplyResult, StandardValueRequirementImpl


# ----------------------------------------------------------------------
class MergeCommitMessage(StandardValueRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(MergeCommitMessage, self).__init__(
            "MergeCommitMessage",
            "BLANK",
            "settings",
            "Pull Requests",
            "Allow merge commits -> Default...",
            _GetValue,
            textwrap.dedent(
                """\
                Available values:

                PR_TITLE [Default message]
                    Pull Request number and head branch on the first line; pull request title on the third line

                BLANK [Default to pull request title]
                    Pull Request title and number on the first line.

                PR_BODY [Default to pull request title and description]
                    Pull Request title and number on the first line; pull request description starting on the third line.

            The default setting is BLANK.

            Reasons for this Default
            ------------------------
            - Reduce redundant information by only duplicating the title of the commit(s).
            - PR_TITLE includes the head branch name, which oftentimes is not relevant information to preserve over time.
            - PR_BODY duplicates the title and description of the commit(s).

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

    result = data.get("allow_merge_commit", None)
    if result is None:
        return None

    if not result:
        return DoesNotApplyResult("Merge commits are not enabled.")

    return data.get("merge_commit_message", None)
