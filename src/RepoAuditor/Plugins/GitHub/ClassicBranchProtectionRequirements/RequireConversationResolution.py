# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireConversationResolution object."""

import textwrap

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicEnableRequirementImpl import (
    ClassicEnableRequirementImpl,
)


# ----------------------------------------------------------------------
class RequireConversationResolution(ClassicEnableRequirementImpl):
    """Require conversation resolution before merging."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "RequireConversationResolution",
            True,
            "disabled",
            "Protect matching branches",
            "Require conversation resolution before merging",
            lambda data: data["branch_protection_data"]["required_conversation_resolution"]["enabled"],
            textwrap.dedent(
                """\
                The default behavior is to require conversation resolution before merging a pull request.

                Reasons for this Default
                ------------------------
                - Conversation resolution is an important part of the development process.
                - Prevent the accidental merging of a pull request before changes associated with the comments have been made.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )
