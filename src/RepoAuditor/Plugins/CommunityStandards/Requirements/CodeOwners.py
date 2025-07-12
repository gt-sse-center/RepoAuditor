# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CodeOwners requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class CodeOwners(ExistsRequirementImpl):
    """Validates that CODEOWNERS file is configured."""

    def __init__(self) -> None:
        super().__init__(
            "CodeOwners",
            "CODEOWNERS",
            [
                ".github/CODEOWNERS",
                "docs/CODEOWNERS",
                "CODEOWNERS",
            ],
            textwrap.dedent(
                """\
                1) Create a CODEOWNERS file in one of these locations:
                   - .github/CODEOWNERS
                   - docs/CODEOWNERS
                   - CODEOWNERS

                Example CODEOWNERS file format:
                # Syntax example:
                # directory/ @username
                # *.js @username
                # /docs/ @username @username2
                """
            ),
            textwrap.dedent(
                """\
                CODEOWNERS files define who is responsible for code review.

                Benefits:
                - Automatic reviewer assignment
                - Clear code ownership
                - Streamlined review process
                """
            ),
        )
