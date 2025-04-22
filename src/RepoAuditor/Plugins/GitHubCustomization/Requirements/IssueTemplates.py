# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the IssueTemplates requirement"""

from pathlib import Path
from typing import Any

from dbrownell_Common.Types import override

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class IssueTemplates(Requirement):
    """Requirement that checks for the presence of issue templates."""

    def __init__(self) -> None:
        super(IssueTemplates, self).__init__(
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
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        try:
            repo_path = query_data.get("repo_path")
            if not repo_path:
                return Requirement.EvaluateImplResult(
                    EvaluateResult.Error,
                    "Repository path not provided.",
                )

            # Ensure repo_path is a Path object
            if isinstance(repo_path, str):
                repo_path = Path(repo_path)

            # Check for issue templates directory
            issue_templates_dir = repo_path / ".github" / "ISSUE_TEMPLATE"

            if issue_templates_dir.exists() and issue_templates_dir.is_dir():
                # Check if there are any template files
                template_files = list(issue_templates_dir.glob("*.md")) + list(
                    issue_templates_dir.glob("*.yml")
                )

                if template_files:
                    return Requirement.EvaluateImplResult(
                        EvaluateResult.Success,
                        f"Found {len(template_files)} issue template(s) in directory.",
                    )
                else:
                    return Requirement.EvaluateImplResult(
                        EvaluateResult.Warning,
                        "Issue templates directory exists but contains no template files.",
                        provide_resolution=True,
                    )

            # Check for single issue template file
            single_template = repo_path / ".github" / "ISSUE_TEMPLATE.md"
            if single_template.exists():
                return Requirement.EvaluateImplResult(
                    EvaluateResult.Success,
                    "Found single issue template file.",
                )

            # No templates found
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                "No issue templates found.",
                provide_resolution=True,
                provide_rationale=True,
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"Error evaluating issue templates: {str(e)}",
            )
