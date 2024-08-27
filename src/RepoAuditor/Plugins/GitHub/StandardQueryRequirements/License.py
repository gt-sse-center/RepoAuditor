# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the License object"""

import textwrap

from typing import Any, Optional

from .Impl.StandardValueRequirementImpl import StandardValueRequirementImpl


# ----------------------------------------------------------------------
class License(StandardValueRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(License, self).__init__(
            "License",
            "MIT License",
            "settings",
            None,
            None,
            _GetValue,
            textwrap.dedent(
                """\
                The default behavior is to use the MIT License.

                Reasons for this Default
                ------------------------
                - The MIT License is a permissive license that allows for the use of the code in any way and
                  a reasonable default for open source software.

                Reasons to Override this Default
                --------------------------------
                - There are many good open source licenses and the MIT License may not be appropriate in all scenarios.
                """,
            ),
        )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(data: dict[str, Any]) -> Optional[str]:
    # Differentiate between "license is not set" and "license cannot be returned due to PAT"
    data = data["standard"]

    if "license" not in data:
        return None

    data = data["license"]
    if data is None:
        return ""

    return data["name"]
