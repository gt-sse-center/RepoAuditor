# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Citation requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class Citation(ExistsRequirementImpl):
    """Validates that a CITATION file is present which is used to make the repository citable.

    Details of how GitHub looks for citation files can be found here: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
    """

    def __init__(self) -> None:
        super().__init__(
            "Citation",
            filename="CITATION",
            possible_locations=[
                # GitHub requires the citation file be in the root directory
                "CITATION.cff",
                "CITATION",
                "CITATIONS",
                "CITATION.bib",
                "CITATIONS.bib",
                "CITATION.md",
                "CITATIONS.md",
                "citation.cff",
                "citation",
                "citations",
                "citation.bib",
                "citations.bib",
                "citation.md",
                "citations.md",
                # R packages are located in the `inst` directory
                "inst/CITATION",
            ],
            resolution=textwrap.dedent(
                """\
                1) Create a CITATION/CITATIONS file in in the root directory.

                2) It can have any of the following extensions:
                   - [blank] e.g. `CITATION`
                   - CITATION.cff
                   - CITATION.md
                   - CITATION.bib
                """
            ),
            rationale=textwrap.dedent(
                """\
                A citation file helps users correctly cite your software.

                For more details, please see
                https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
                """
            ),
            dynamic_arg_name="unrequired",
        )
