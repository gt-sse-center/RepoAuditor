# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SupportDiscussions object"""

import textwrap

from .Impl.StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class SupportDiscussions(StandardEnableRequirementImpl):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SupportDiscussions, self).__init__(
            "SupportDiscussions",
            False,
            "true",
            "settings",
            "Features",
            "Discussions",
            lambda data: data["standard"].get("has_discussions", None),
            rationale=textwrap.dedent(
                """\
                No rationale for this default.
                """,
            ),
            subject="Support for Discussions",
        )
