# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the AllowForcePushes object"""

import textwrap

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class AllowForcePushes(ClassicEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(AllowForcePushes, self).__init__(
            "AllowForcePushes",
            False,
            "true",
            "Rules applied to everyone including administrators",
            "Allow force pushes",
            lambda data: data["branch_protection_data"]["allow_force_pushes"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to not allow force pushes to the mainline branch.

                Reasons for this Default
                ------------------------
                - Force pushes rewrite history, which breaks git lineage for all other clones of the repository.
                  Merges are possible when this happens, but they are difficult to perform and data loss is
                  possible.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
