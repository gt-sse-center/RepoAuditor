# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SecurityPolicy requirement."""

import textwrap

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class SecurityPolicy(ExistsRequirementImpl):
    """Validates that a security policy is configured."""

    def __init__(self) -> None:
        super().__init__(
            "SecurityPolicy",
            "SECURITY",
            [
                ".github/SECURITY.md",
                "docs/SECURITY.md",
                "SECURITY.md",
            ],
            textwrap.dedent(
                """\
                1) Create a security policy file in one of these locations:
                   - .github/SECURITY.md
                   - docs/SECURITY.md
                   - SECURITY.md

                Example policy can be found at:
                https://github.com/gt-sse-center/RepoAuditor/blob/main/SECURITY.md
                """
            ),
            textwrap.dedent(
                """\
                Security policies help users report vulnerabilities responsibly.

                Benefits:
                - Clear security reporting process
                - Responsible disclosure guidelines
                - Better security management
                """
            ),
        )
