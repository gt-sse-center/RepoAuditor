# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SecretScanningPushProtection object"""

import textwrap

from typing import Any, Optional

from .StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class SecretScanningPushProtection(
    StandardEnableRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SecretScanningPushProtection, self).__init__(
            "SecretScanningPushProtection",
            True,
            "false",
            "settings/security_analysis",
            "Secret scanning",
            "Push protection",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to enable secret scanning push protection.

                Reasons for this Default
                ------------------------
                - Secrets should not be checked into code.

                Reasons to Override this Default
                --------------------------------
                <unknown>
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
        .get("secret_scanning_push_protection", {})
        .get("status", None)
    )

    if result is None:
        return None

    return result == "enabled"
