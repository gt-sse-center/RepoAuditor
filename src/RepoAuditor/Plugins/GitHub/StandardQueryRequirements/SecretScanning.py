# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the SecretScanning object"""

import textwrap

from typing import Any, Optional

from ..Impl.EnableRequirementImpl import EnableRequirementImpl


# ----------------------------------------------------------------------
class SecretScanning(EnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SecretScanning, self).__init__(
            "SecretScanning",
            True,
            "false",
            "settings/security_analysis",
            "Secret scanning",
            "Secret scanning",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to enable secret scanning.

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
        .get("secret_scanning", {})
        .get("status", None)
    )

    if result is None:
        return None

    return result == "enabled"
