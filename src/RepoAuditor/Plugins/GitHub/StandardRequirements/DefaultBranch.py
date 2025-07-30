# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the DefaultBranch object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardValueRequirementImpl import (
    StandardValueRequirementImpl,
)


# ----------------------------------------------------------------------
class DefaultBranch(StandardValueRequirementImpl):
    """Requirement of a default branch in the repository."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "DefaultBranch",
            "main",
            "settings",
            "Default Branch",
            "Default Branch",
            lambda data: data["standard"].get("default_branch", None),
            textwrap.dedent(
                """\
                The default behavior is not name the mainline/base/default branch "main".

                Reasons for this Default
                ------------------------
                - Eliminate divisive language in favor of non-divisive language, this includes eliminating
                  the use of terms that were inappropriately and offensively taken from slavery including
                  the elimination of the term master in favor of main.

                  https://www.linkedin.com/pulse/technology-notes-how-tos-infrastructure-git-master-main-eldritch/

                Reasons to Override this Default
                --------------------------------
                - You are validating a legacy repository that still uses 'master' as the mainline/base/default branch.
                """,
            ),
        )
