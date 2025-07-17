# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Contributing requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class Contributing(ExistsRequirementImpl):
    """Validates that a contributing guide is configured."""

    def __init__(self) -> None:
        super().__init__(
            "Contributing",
            "CONTRIBUTING",
            [
                ".github/CONTRIBUTING.md",
                "docs/CONTRIBUTING.md",
                "CONTRIBUTING.md",
            ],
            textwrap.dedent(
                """\
                1) Create a contributing guide in one of these locations:
                   - .github/CONTRIBUTING.md
                   - docs/CONTRIBUTING.md
                   - CONTRIBUTING.md

                Example template can be found at:
                https://github.com/nayafia/contributing-template/blob/master/CONTRIBUTING-template.md
                """
            ),
            textwrap.dedent(
                """\
                Contributing guides help new contributors understand how to participate.

                Benefits:
                - Clear contribution process
                - Consistent code quality
                - Better community engagement
                """
            ),
        )
