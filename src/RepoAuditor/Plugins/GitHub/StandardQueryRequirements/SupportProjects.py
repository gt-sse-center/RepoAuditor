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
class SupportProjects(StandardEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SupportProjects, self).__init__(
            "SupportProjects",
            True,
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
            subject="Support for Projects",
        )
