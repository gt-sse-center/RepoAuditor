# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CodeOwners requirement"""

import textwrap
from pathlib import Path
from typing import Any

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class CodeOwners(Requirement):
    """Validates that CODEOWNERS file is configured."""

    def __init__(self):
        super(CodeOwners, self).__init__(
            "CodeOwners",
            "Validates that CODEOWNERS file is configured.",
            ExecutionStyle.Parallel,
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

    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        repo_path = query_data["repo_path"]

        # Check all possible locations for CODEOWNERS file
        possible_locations = [
            repo_path / ".github" / "CODEOWNERS",
            repo_path / "docs" / "CODEOWNERS",
            repo_path / "CODEOWNERS",
        ]

        for location in possible_locations:
            if location.exists():
                return Requirement.EvaluateImplResult(EvaluateResult.Success, None)

        return Requirement.EvaluateImplResult(
            EvaluateResult.Error,
            "No CODEOWNERS file found.",
            provide_resolution=True,
            provide_rationale=True,
        )
