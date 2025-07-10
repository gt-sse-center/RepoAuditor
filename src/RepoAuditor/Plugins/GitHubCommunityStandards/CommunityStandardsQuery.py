# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CommunityStandardsQuery object."""

from tempfile import TemporaryDirectory
from typing import Any, Optional
from urllib.parse import urlparse

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
        branch = module_data.get("branch", "main")
        temp_repo_dir = TemporaryDirectory()
        github_url = module_data["url"]

        # Add PAT to GitHub URL, if present
        github_pat = module_data.get("pat")
        if github_pat:
            url = urlparse(github_url)
            github_url = f"https://{github_pat}@{url.netloc}{url.path}"

        # Import git.Repo here so that it is only imported
        # if the GitHubCommunityStandards plugin is requested.
        from git import Repo

        try:
            Repo.clone_from(github_url, temp_repo_dir.name, branch=branch)
        except Exception as e:
            error_msg = f"""
            An error occurred while attempting to clone the target repository.
            If you are auditing a private repository, {
                "please ensure your PAT has access to the repository."
                if github_pat
                else "please provide a PAT with access to the repository."
            }
            Error: {e}
            """
            raise RuntimeError(error_msg) from e

        # Record the path and the temp directory for later cleanup
        module_data["repo_dir"] = temp_repo_dir

        return module_data

    @override
    def Cleanup(self, module_data: dict[str, Any]) -> None:
        """Clean up the cloned repository."""
        repo_dir = module_data["repo_dir"]
        repo_dir.cleanup()
        del module_data
