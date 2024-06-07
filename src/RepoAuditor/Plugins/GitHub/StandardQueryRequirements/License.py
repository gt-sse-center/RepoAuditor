# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the License object"""

import textwrap

from ..Impl.ValueRequirementImpl import ValueRequirementImpl


# ----------------------------------------------------------------------
class License(ValueRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(License, self).__init__(
            "License",
            "MIT License",
            "settings",
            None,
            None,
            lambda data: data["standard"].get("license", {}).get("name", None),
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
