# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the WebCommitSignoff object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class WebCommitSignoff(StandardEnableRequirementImpl):
    """Require contributors to sign off on web-based commits."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "WebCommitSignoff",
            True,
            "disabled",
            "settings",
            "General",
            "Require contributors to sign off on web-based commits",
            lambda data: data["standard"].get("web_commit_signoff_required", None),
            rationale=textwrap.dedent(
                """\
                The default behavior is to require contributors to sign off on web-based commits.

                Reasons for this Default
                ------------------------
                - All changes (regardless of where they were made) should go through the same validation process.

                Reasons to Override this Default
                --------------------------------
                - Changes made via the web interface are considered to be benign and should not be subject to
                  the standard validation process.
                """,
            ),
        )
