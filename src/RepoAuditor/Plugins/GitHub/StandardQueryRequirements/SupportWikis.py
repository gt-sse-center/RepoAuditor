# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SupportWikis object"""

import textwrap

from .Impl.StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class SupportWikis(StandardEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SupportWikis, self).__init__(
            "SupportWikis",
            True,
            "false",
            "settings",
            "Features",
            "Wikis",
            lambda data: data["standard"].get("has_wiki", None),
            rationale=textwrap.dedent(
                """\
                No rationale for this default.
                """,
            ),
            subject="Support for Wikis",
        )
