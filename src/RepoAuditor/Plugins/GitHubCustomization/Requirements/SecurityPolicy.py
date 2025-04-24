# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the SecurityPolicy requirement"""

import textwrap
from pathlib import Path
from typing import Any

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class SecurityPolicy(Requirement):
    """Validates that a security policy is configured."""

    def __init__(self):
        super(SecurityPolicy, self).__init__(
            "SecurityPolicy",
            "Validates that a security policy is configured.",
            ExecutionStyle.Parallel,
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

    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        repo_path = query_data["repo_path"]

        # Check all possible locations for security policy
        possible_locations = [
            repo_path / ".github" / "SECURITY.md",
            repo_path / "docs" / "SECURITY.md",
            repo_path / "SECURITY.md",
        ]

        for location in possible_locations:
            if location.exists():
                return Requirement.EvaluateImplResult(EvaluateResult.Success, None)

        return Requirement.EvaluateImplResult(
            EvaluateResult.Error,
            "No security policy found.",
            provide_resolution=True,
            provide_rationale=True,
        )
