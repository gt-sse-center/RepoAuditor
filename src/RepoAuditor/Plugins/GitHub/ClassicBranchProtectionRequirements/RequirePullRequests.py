# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequirePullRequests object."""

import textwrap

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicEnableRequirementImpl import (
    ClassicEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class RequirePullRequests(ClassicEnableRequirementImpl):
    """Require a pull request before merging."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "RequirePullRequests",
            True,
            "disabled",
            "Protect matching branches",
            "Require a pull request before merging",
            lambda data: "required_pull_request_reviews" in data["branch_protection_data"],
            textwrap.dedent(
                """\
                The default behavior is to require pull requests before merging.

                Reasons for this Default
                ------------------------
                - Pull requests are an important part of the development process and prevent unwanted changes from
                  making it into the mainline branch.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
