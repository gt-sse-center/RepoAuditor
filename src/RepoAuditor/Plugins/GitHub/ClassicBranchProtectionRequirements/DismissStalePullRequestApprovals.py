# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the DismissStalePullRequestApprovals object"""

import textwrap

from typing import Any, Optional

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class DismissStalePullRequestApprovals(
    ClassicEnableRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(DismissStalePullRequestApprovals, self).__init__(
            "DismissStalePullRequestApprovals",
            True,
            "false",
            "Protect matching branches",
            "Require a pull request before merging -> Dismiss stale pull request approvals when new commits are pushed",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to dismiss stale pull request approvals when new commits are pushed.

                Reasons for this Default
                ------------------------
                - Approvals apply to the changes as they existed when the approval was granted. The approval
                  may no longer be valid when new changes are pushed.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """
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

    return settings["dismiss_stale_reviews"]
