# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the PullRequestTemplate requirement."""

from pathlib import Path
from typing import Any

from dbrownell_Common.Types import override

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class PullRequestTemplate(Requirement):
    """Validates that a pull request template is configured."""

    def __init__(self) -> None:
        super().__init__(
            "PullRequestTemplate",
            "Validates that a pull request template is configured.",
            ExecutionStyle.Parallel,
            "Create a pull request template file in one of these locations: .github/PULL_REQUEST_TEMPLATE.md, .github/pull_request_template.md, docs/PULL_REQUEST_TEMPLATE.md, or PULL_REQUEST_TEMPLATE.md",
            "Pull request templates help standardize code contributions and expedite the review process by ensuring consistent PR format.",
        )

    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],  # noqa: ARG002
    ) -> Requirement.EvaluateImplResult:
        repo_path = query_data.get("repo_path")
        if not repo_path:
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                "Repository path not provided.",
            )

        # Ensure repo_path is a Path object
        if isinstance(repo_path, str):
            repo_path = Path(repo_path)

        # Check all possible locations for PR template
        possible_locations = [
            # Upper case variants
            repo_path / ".github" / "PULL_REQUEST_TEMPLATE.md",
            repo_path / "docs" / "PULL_REQUEST_TEMPLATE.md",
            repo_path / "PULL_REQUEST_TEMPLATE.md",
            # Lower case variants
            repo_path / ".github" / "pull_request_template.md",
            repo_path / "docs" / "pull_request_template.md",
            repo_path / "pull_request_template.md",
            # Directory with multiple templates
            repo_path / ".github" / "PULL_REQUEST_TEMPLATE",
            repo_path / ".github" / "pull_request_template",
        ]

        for location in possible_locations:
            if location.exists():
                if location.is_dir():
                    # If it's a directory, check if it contains templates
                    templates = list(location.glob("*.md"))
                    if templates:
                        return Requirement.EvaluateImplResult(
                            EvaluateResult.Success,
                            f"Found pull request templates in {location.relative_to(repo_path)}",
                        )
                else:
                    return Requirement.EvaluateImplResult(
                        EvaluateResult.Success,
                        f"Found pull request template at {location.relative_to(repo_path)}",
                    )

        return Requirement.EvaluateImplResult(
            EvaluateResult.Error,
            "No pull request template found.",
            provide_resolution=True,
            provide_rationale=True,
        )
