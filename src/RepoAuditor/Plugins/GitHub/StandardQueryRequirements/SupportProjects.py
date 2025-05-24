# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SupportProjects object"""

import textwrap

from .Impl.StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class SupportProjects(StandardEnableRequirementImpl):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SupportProjects, self).__init__(
            "SupportProjects",
            "false",
            "settings",
            "Features",
            "Projects",
            lambda data: data["standard"].get("has_projects", None),
            rationale=textwrap.dedent(
                """\
                No rationale for this default.
                """,
            ),
            default_value=True,
            subject="Support for Projects",
        )
