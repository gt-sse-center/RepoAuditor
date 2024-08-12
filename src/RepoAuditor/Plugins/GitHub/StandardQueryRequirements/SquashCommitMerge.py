# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SquashCommitMerge object"""

import textwrap

from ..Impl.EnableRequirementImpl import EnableRequirementImpl


# ----------------------------------------------------------------------
class SquashCommitMerge(EnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(SquashCommitMerge, self).__init__(
            "SquashCommitMerge",
            False,
            "true",
            "settings",
            "Pull Requests",
            "Allow squash merging",
            lambda data: data["standard"].get("allow_squash_merge", None),
            textwrap.dedent(
                """\
                The default behavior is to not allow squash merging.

                Reasons for this Default
                ------------------------
                - Rebase merging is not compatible with signed commits, as GitHub creates a new commit when squashing.

                Reasons to Override this Default
                --------------------------------
                - Your repository does not require signatures.
                - You want to ensure that single-commit-changes are merged into the mainline branch to simplify the branch's history.
                """,
            ),
        )
