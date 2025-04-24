# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Contributing requirement"""

import textwrap
from pathlib import Path
from typing import Any

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class Contributing(Requirement):
    """Validates that a contributing guide is configured."""

    def __init__(self):
        super(Contributing, self).__init__(
            "Contributing",
            "Validates that a contributing guide is configured.",
            ExecutionStyle.Parallel,
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

    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        repo_path = query_data["repo_path"]

        # Check all possible locations for contributing guide
        possible_locations = [
            repo_path / ".github" / "CONTRIBUTING.md",
            repo_path / "docs" / "CONTRIBUTING.md",
            repo_path / "CONTRIBUTING.md",
        ]

        for location in possible_locations:
            if location.exists():
                return Requirement.EvaluateImplResult(EvaluateResult.Success, None)

        return Requirement.EvaluateImplResult(
            EvaluateResult.Error,
            "No contributing guide found.",
            provide_resolution=True,
            provide_rationale=True,
        )
