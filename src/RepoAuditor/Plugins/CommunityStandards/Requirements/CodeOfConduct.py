# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CodeOfConduct requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class CodeOfConduct(ExistsRequirementImpl):
    """Validates that a CODE_OF_CONDUCT file is configured."""

    def __init__(self) -> None:
        super().__init__(
            "CodeOfConduct",
            "CODE_OF_CONDUCT",
            [
                ".github/CODE_OF_CONDUCT",
                ".github/CODE_OF_CONDUCT.md",
                ".github/CODE_OF_CONDUCT.rst",
                "docs/CODE_OF_CONDUCT",
                "docs/CODE_OF_CONDUCT.md",
                "docs/CODE_OF_CONDUCT.rst",
                "CODE_OF_CONDUCT",
                "CODE_OF_CONDUCT.md",
                "CODE_OF_CONDUCT.rst",
            ],
            textwrap.dedent(
                """\
                1) Create a CODE_OF_CONDUCT file in one of these locations:
                   - .github/CODE_OF_CONDUCT
                   - docs/CODE_OF_CONDUCT
                   - CODE_OF_CONDUCT

                Example CODE_OF_CONDUCT file format:
                ```
                # Contributor Code of Conduct
                ## Principles
                ## Community Guidelines
                ```
                """
            ),
            textwrap.dedent(
                """\
                A CODE_OF_CONDUCT defines expectations for behavior for your
                project's participants.

                Benefits:
                - Define community standards
                - Signal a welcoming and inclusive project
                - Outline procedures for handling abuse
                - Help create a positive social atmosphere for your community
                """
            ),
        )
