# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SupportIssues object"""

import textwrap

from .Impl.StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class SupportIssues(StandardEnableRequirementImpl):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SupportIssues, self).__init__(
            "SupportIssues",
            True,
            "false",
            "settings",
            "Features",
            "Issues",
            lambda data: data["standard"].get("has_issues", None),
            rationale=textwrap.dedent(
                """\
                No rationale for this default.
                """,
            ),
            subject="Support for Issues",
        )
