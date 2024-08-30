# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireStatusChecksToPass object"""

import textwrap

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class RequireStatusChecksToPass(
    ClassicEnableRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(RequireStatusChecksToPass, self).__init__(
            "RequireStatusChecksToPass",
            True,
            "false",
            "Protect matching branches",
            "Require status checks to pass before merging",
            lambda data: "required_status_checks" in data["branch_protection_data"],
            textwrap.dedent(
                """\
                The default behavior is to require status checks to pass before merging a pull request.

                Reasons for this Default
                ------------------------
                - Status checks are an important part of the development process and should not be bypassed.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
