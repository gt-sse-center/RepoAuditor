# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireUpToDateBranches object"""

import textwrap

from typing import Any, Optional

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class RequireUpToDateBranches(
    ClassicEnableRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(RequireUpToDateBranches, self).__init__(
            "RequireUpToDateBranches",
            True,
            "false",
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

    return settings["strict"]
