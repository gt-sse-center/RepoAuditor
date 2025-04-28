# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the IssueTemplates requirement."""

from pathlib import Path
from typing import Any

from dbrownell_Common.Types import override

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class IssueTemplates(Requirement):
    """Requirement that checks for the presence of issue templates."""

    def __init__(self) -> None:
        super().__init__(
            "IssueTemplates",
            "Validates that the repository has issue templates.",
            ExecutionStyle.Parallel,
            "Add issue templates to your repository in the .github/ISSUE_TEMPLATE directory.",
            "Issue templates help contributors create high-quality issues by providing a structured format.",
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

        # Check for issue templates directories (both upper and lowercase)
        issue_templates_dirs = [
            repo_path / ".github" / "ISSUE_TEMPLATE",
            repo_path / ".github" / "issue_template",
        ]

        for issue_templates_dir in issue_templates_dirs:
            if issue_templates_dir.exists() and issue_templates_dir.is_dir():
                # Check if there are any template files
                template_files = list(issue_templates_dir.glob("*.md")) + list(
                    issue_templates_dir.glob("*.yml")
                )

                if template_files:
                    return Requirement.EvaluateImplResult(
                        EvaluateResult.Success,
                        f"Found {len(template_files)} issue template(s) in directory {issue_templates_dir.relative_to(repo_path)}.",
                    )

                return Requirement.EvaluateImplResult(
                    EvaluateResult.Warning,
                    f"Issue templates directory {issue_templates_dir.relative_to(repo_path)} exists but contains no template files.",
                    provide_resolution=True,
                )

        # Check for single issue template files (both upper and lowercase)
        single_templates = [
            repo_path / ".github" / "ISSUE_TEMPLATE.md",
            repo_path / "docs" / "ISSUE_TEMPLATE.md",
            repo_path / "ISSUE_TEMPLATE.md",
            repo_path / "docs" / "issue_template.md",
            repo_path / ".github" / "issue_template.md",
            repo_path / "issue_template.md",
        ]

        for single_template in single_templates:
            if single_template.exists():
                return Requirement.EvaluateImplResult(
                    EvaluateResult.Success,
                    f"Found single issue template file at {single_template.relative_to(repo_path)}.",
                )

        # No templates found
        return Requirement.EvaluateImplResult(
            EvaluateResult.Error,
            "No issue templates found.",
            provide_resolution=True,
            provide_rationale=True,
        )
