# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the IssueTemplates requirement."""

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class IssueTemplates(ExistsRequirementImpl):
    """Requirement that checks for the presence of issue templates."""

    def __init__(self) -> None:
        super().__init__(
            "IssueTemplates",
            "ISSUE_TEMPLATES",
            [
                ".github/ISSUE_TEMPLATE.md",
                "docs/ISSUE_TEMPLATE.md",
                "ISSUE_TEMPLATE.md",
                ".github/issue_template.md",
                "docs/issue_template.md",
                "issue_template.md",
                # Directories
                ".github/ISSUE_TEMPLATE",
            ],
            "Add issue templates to your repository in the .github/ISSUE_TEMPLATE directory.",
            "Issue templates help contributors create high-quality issues by providing a structured format.",
        )
