# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CustomizationQuery object."""

from tempfile import TemporaryDirectory
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]
from git import Repo

from RepoAuditor.Plugins.GitHubCustomization.Requirements.CodeOwners import CodeOwners
from RepoAuditor.Plugins.GitHubCustomization.Requirements.Contributing import Contributing
from RepoAuditor.Plugins.GitHubCustomization.Requirements.IssueTemplates import IssueTemplates
from RepoAuditor.Plugins.GitHubCustomization.Requirements.PullRequestTemplates import PullRequestTemplate
from RepoAuditor.Plugins.GitHubCustomization.Requirements.SecurityPolicy import SecurityPolicy
from RepoAuditor.Query import ExecutionStyle, Query


class CustomizationQuery(Query):
    """Query with requirements that check for GitHub customization files."""

    def __init__(self) -> None:
        super().__init__(
            "CustomizationQuery",
            ExecutionStyle.Parallel,
            [
                CodeOwners(),
                Contributing(),
                IssueTemplates(),
                PullRequestTemplate(),
                SecurityPolicy(),
            ],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Get the repo data."""

        # Clone the GitHub repository to a temp directory
        github_url = module_data["url"]
        branch = module_data.get("branch", "main")
        temp_repo_dir = TemporaryDirectory()
        Repo.clone_from(github_url, temp_repo_dir.name, branch=branch)

        # Record the path and the temp directory for later cleanup
        module_data["repo_dir"] = temp_repo_dir

        return module_data

    @override
    def Cleanup(self, module_data: dict[str, Any]) -> None:
        """Clean up the cloned repository."""
        repo_dir = module_data["repo_dir"]
        repo_dir.cleanup()
        del module_data
