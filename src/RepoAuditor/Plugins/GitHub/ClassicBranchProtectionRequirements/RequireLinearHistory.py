# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireLinearHistory object"""

import textwrap

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class RequireLinearHistory(ClassicEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(RequireLinearHistory, self).__init__(
            "RequireLinearHistory",
            False,
            "true",
            "Protect matching branches",
            "Require linear history",
            lambda data: data["branch_protection_data"]["required_linear_history"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to not require a linear history as this option is disabled when rebase
                merging and squash merging are disabled (which are the default validation settings).

                Reasons for this Default
                ------------------------
                - This option is disabled within the GitHub UX when rebase merging and squash merging are disabled
                  (which are the default validation settings).

                Reasons to Override this Default
                --------------------------------
                - You have enabled rebase merging or squash merging
                """,
            ),
        )
