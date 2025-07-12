# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ReadMe requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class ReadMe(ExistsRequirementImpl):
    """Validates that a README file is configured."""

    def __init__(self) -> None:
        super().__init__(
            "ReadMe",
            "README",
            [
                "README.md",
            ],
            textwrap.dedent(
                """\
                Create a README.md file in the root of the repository.

                Example READMEs can be found at https://github.com/matiassingers/awesome-readme
                """
            ),
            textwrap.dedent(
                """\
                A README file provides the first point of entry into using
                and contributing to the repository.

                Benefits:
                - Summarizes repository.
                - Instructions on how to install and run the code.
                - Provides links to more information.
                """
            ),
        )
