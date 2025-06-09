# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireApprovals object."""

import textwrap
from typing import Any

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicValueRequirementImpl import (
    ClassicValueRequirementImpl,
    DoesNotApplyResult,
)


# ----------------------------------------------------------------------
class RequireApprovals(ClassicValueRequirementImpl):
    """Require approvals for pull requests."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "RequireApprovals",
            "1",
            "Protect matching branches",
            "Require a pull request before merging -> Require approvals",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to require at least one approval.

                Reasons for this Default
                ------------------------
                - Code Reviews are a generally accepted best practice for software development.

                Reasons to Override this Default
                --------------------------------
                - You are the only person working on the repository (set the value to 0).
                - You want to require more than one approval (set the value to the number of approvals required).
                - You are not comfortable with the amount of time code reviews introduce in the development process (set the value to 0).
                """,
            ),
        )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(
    data: dict[str, Any],
) -> str | DoesNotApplyResult | None:
    settings = data["branch_protection_data"].get("required_pull_request_reviews", None)
    if settings is None:
        return None

    return settings.get("required_approving_review_count", None)
