# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the DependabotSecurityUpdates object"""

import textwrap

from typing import Any, Optional

from .StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class DependabotSecurityUpdates(
    StandardEnableRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(DependabotSecurityUpdates, self).__init__(
            "DependabotSecurityUpdates",
            True,
            "false",
            "settings/security_analysis",
            "Dependabot",
            "Dependabot security updates",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to enable Dependabot security updates.

                Reasons for this Default
                ------------------------
                - Increases the overall security of the repository by automatically applying security updates.

                Reasons to Override this Default
                --------------------------------
                - Dependabot security updates are not supported for the repository or by the organization.
                - A manual test pass is required before changes can be deployed.
                """,
            ),
            unset_set_terminology=("disabled", "enabled"),
        )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(data: dict[str, Any]) -> Optional[bool]:
    result = (
        data["standard"]
        .get("security_and_analysis", {})
        .get("dependabot_security_updates", {})
        .get("status", None)
    )

    if result is None:
        return None

    return result == "enabled"
