# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireUpToDateBranches object."""

import textwrap
from typing import Any, Optional

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicEnableRequirementImpl import (
    ClassicEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class RequireUpToDateBranches(ClassicEnableRequirementImpl):
    """Require branches to be up to date before merging."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "RequireUpToDateBranches",
            True,
            "disabled",
            "Protect matching branches",
            "Require status checks to pass before merging -> Require branches to be up to date before merging",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to require branches to be up to date before merging. The terminology
                used by GitHub is a bit confusing, as this setting ensures that all GitHub workflows triggered
                by the pull request have completed successfully before the pull request can be merged.

                Reasons for this Default
                ------------------------
                - Workflows run should pass before a pull request is merged into the mainline branch.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(
    data: dict[str, Any],
) -> Optional[bool]:
    settings = data["branch_protection_data"].get("required_status_checks", None)
    if settings is None:
        return None

    return settings.get("strict", None)
