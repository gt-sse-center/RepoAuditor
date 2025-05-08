# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireApprovalMostRecentPush object"""

import textwrap

from typing import Any, Optional

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class RequireApprovalMostRecentPush(ClassicEnableRequirementImpl):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(RequireApprovalMostRecentPush, self).__init__(
            "RequireApprovalMostRecentPush",
            True,
            "false",
            "Protect matching branches",
            "Require a pull request before merging -> Require approval of the most recent reviewable push",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to require approval of the most recent reviewable push by someone other than the author of the pull request.

                Reasons for this Default
                ------------------------
                - Self-approval of a pull request eliminates the value provided by a second pair of eyes during a code review.

                Reasons to Override this Default
                --------------------------------
                - You are the only person working on the repository.
                """,
            ),
        )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(
    data: dict[str, Any],
) -> Optional[bool]:
    settings = data["branch_protection_data"].get("required_pull_request_reviews", None)
    if settings is None:
        return None

    return settings["require_last_push_approval"]
