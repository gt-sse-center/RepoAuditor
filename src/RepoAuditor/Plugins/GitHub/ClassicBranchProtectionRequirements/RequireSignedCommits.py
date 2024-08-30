# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireSignedCommits object"""

import textwrap

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class RequireSignedCommits(ClassicEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(RequireSignedCommits, self).__init__(
            "RequireSignedCommits",
            True,
            "false",
            "Protect matching branches",
            "Require signed commits",
            lambda data: data["branch_protection_data"]["required_signatures"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to require signed commits. Note that this setting does not work with
                rebase merging or squash merging.

                Reasons for this Default
                ------------------------
                - Ensure that the author of a commit is who the claim to be.

                Reasons to Override this Default
                --------------------------------
                - You have enabled rebase merging or squash merging.
                """,
            ),
        )
