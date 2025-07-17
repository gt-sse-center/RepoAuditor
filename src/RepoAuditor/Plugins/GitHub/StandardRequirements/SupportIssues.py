# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SupportIssues object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class SupportIssues(StandardEnableRequirementImpl):
    """Support for Issues."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "SupportIssues",
            True,
            "disabled",
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
