# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the AllowDeletions object"""

import textwrap

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class AllowDeletions(ClassicEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(AllowDeletions, self).__init__(
            "AllowDeletions",
            False,
            "true",
            "Rules applied to everyone including administrators",
            "Allow deletions",
            lambda data: data["branch_protection_data"]["allow_deletions"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to not allow the deletion of the mainline branch.

                Reasons for this Default
                ------------------------
                - Bad things happen when the mainline branch is deleted.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
