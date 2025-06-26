# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CommunityStandardsQuery object."""

from tempfile import TemporaryDirectory
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.CodeOfConduct import CodeOfConduct
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.CodeOwners import CodeOwners
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.Contributing import Contributing
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.IssueTemplates import IssueTemplates
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.LicenseFile import LicenseFile
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.PullRequestTemplates import PullRequestTemplate
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.ReadMe import ReadMe
from RepoAuditor.Plugins.GitHubCommunityStandards.Requirements.SecurityPolicy import SecurityPolicy
from RepoAuditor.Query import ExecutionStyle, Query


class CommunityStandardsQuery(Query):
    """Query with requirements that check for GitHub CommunityStandards files."""

    def __init__(self) -> None:
        super().__init__(
            "CommunityStandardsQuery",
            ExecutionStyle.Parallel,
            [
                CodeOfConduct(),
                CodeOwners(),
                Contributing(),
                IssueTemplates(),
                LicenseFile(),
                PullRequestTemplate(),
                ReadMe(),
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

        # Import git.Repo here so that it is only imported
        # if the GitHubCommunityStandards plugin is requested.
        from git import Repo

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
