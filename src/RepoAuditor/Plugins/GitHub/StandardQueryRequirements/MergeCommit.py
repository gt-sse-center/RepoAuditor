# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the MergeCommit object"""

import textwrap

from ..Impl.EnableRequirementImpl import EnableRequirementImpl


# ----------------------------------------------------------------------
class MergeCommit(EnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(MergeCommit, self).__init__(
            "MergeCommit",
            True,
            "false",
            "settings",
            "Pull Requests",
            "Allow merge commits",
            lambda data: data["standard"].get("allow_merge_commit", None),
            textwrap.dedent(
                """\
                The default behavior is to allow merge commits.

                Reasons for this Default
                ------------------------
                - Merge commits are the most basic way to merge from a branch into another branch.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
