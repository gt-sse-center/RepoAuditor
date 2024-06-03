# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the WebCommitSignoff object"""

import textwrap

from ..Impl.EnableRequirementImpl import EnableRequirementImpl


# ----------------------------------------------------------------------
class WebCommitSignoff(EnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(WebCommitSignoff, self).__init__(
            "WebCommitSignoff",
            True,
            "false",
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
