# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the AllowBypassSettings object"""

import textwrap

from .ClassicBranchProtectionRequirementImpl import ClassicBranchProtectedRequirementImpl


# ----------------------------------------------------------------------
class DoNotAllowBypassSettings(
    ClassicBranchProtectedRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(DoNotAllowBypassSettings, self).__init__(
            "DoNotAllowBypassSettings",
            True,
            "false",
            "Protect matching branches",
            "Do not allow bypassing the above settings",
            lambda data: data["branch_protection_data"]["enforce_admins"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to not allow administrators to bypass branch protection settings.

                Reasons for this Default
                ------------------------
                - Ensure that all pull requests go through the same verification process.

                Reasons to Override this Default
                --------------------------------
                - The steps invoked during the verification process...
                    * ...are unreliable.
                    * ...take an excessive amount of time to complete.

                * Note that all of the reasons in this section are workarounds to address the underlying instability
                  of the steps invoked during the verification process. The ideal solution is to address the
                  underlying instability.
                """,
            ),
        )
