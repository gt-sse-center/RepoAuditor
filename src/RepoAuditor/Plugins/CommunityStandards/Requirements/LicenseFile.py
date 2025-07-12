# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the LicenseFile requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import (
    ExistsRequirementImpl,
)


class LicenseFile(ExistsRequirementImpl):
    """Validates that a CODE_OF_CONDUCT file is configured."""

    def __init__(self) -> None:
        super().__init__(
            "LicenseFile",
            "LICENSE",
            [
                "LICENSE",
                "LICENSE.md",
                "LICENSE.txt",
                "LICENSE.rst",
            ],
            textwrap.dedent(
                """\
                1) Create a LICENSE file in in the root directory.

                2) It can have any of the following extensions:
                   - [blank] e.g. `LICENSE`
                   - LICENSE.md
                   - LICENSE.rst
                   - LICENSE.txt
                """
            ),
            textwrap.dedent(
                """\
                A software license tells others what they can and can't do with your source code.

                https://choosealicense.com/ can help decide which license
                best meets your repository's needs.
                """
            ),
        )
