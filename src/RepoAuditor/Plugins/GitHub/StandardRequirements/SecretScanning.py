# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SecretScanning object."""

import textwrap
from typing import Any, Optional

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class SecretScanning(StandardEnableRequirementImpl):
    """Secret scanning enable requirement."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "SecretScanning",
            True,
            "disabled",
            "settings/security_analysis",
            "Secret Protection",
            "Secret protection",
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to ensure secret protection is enabled.

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
    result = data["standard"].get("security_and_analysis", {}).get("secret_scanning", {}).get("status", None)

    if result is None:
        return None

    return result == "enabled"
