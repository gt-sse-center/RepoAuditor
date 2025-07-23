# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the AutoMerge object."""

import textwrap

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardEnableRequirementImpl import (
    StandardEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class AutoMerge(StandardEnableRequirementImpl):
    """Requirement to enable auto-merge for pull requests."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "AutoMerge",
            True,
            "disabled",
            "settings",
            "Pull Requests",
            "Allow auto-merge",
            lambda data: data["standard"].get("allow_auto_merge", None),
            textwrap.dedent(
                """\
                The default behavior is to enable the option to auto-merge once all the required status checks associated with a pull request have passed.

                Reasons for this Default
                ------------------------
                - Reduces mean resolution time by triggering the merge once all the required status checks pass.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
