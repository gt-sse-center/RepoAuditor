# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the CommunityStandards plugin."""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    InitializeStreamCapabilities,
)
from git import Repo
from typer.testing import CliRunner
from utilities import CheckPATFileExists, GetGithubUrl, ScrubDurationGithuburlAndSpaces

from RepoAuditor.EntryPoint import app
from RepoAuditor.Plugins.CommunityStandards.CommunityStandardsQuery import CommunityStandardsQuery

# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


def GetDataFunctional(path_to_delete: str, is_directory=False):
    """A functional which returns a modified GetData method which
    deletes the specified path in the cloned repo.
    """

    def GetData(self, module_data):
        # Clone the GitHub repository to a temp directory
        github_url = module_data["url"]
        branch = module_data.get("branch", "main")
        temp_repo_dir = TemporaryDirectory()
        Repo.clone_from(github_url, temp_repo_dir.name, branch=branch)

        path = Path(temp_repo_dir.name) / path_to_delete

        if is_directory:
            shutil.rmtree(path)
        else:
            path.unlink()

        # Record the path and the temp directory for later cleanup
        module_data["repo_dir"] = temp_repo_dir
        return module_data

    return GetData


# ----------------------------------------------------------------------
class TestCommunityStandards:
    """End-to-end tests for community standards files in a GitHub repository."""

    # ----------------------------------------------------------------------
    def test_CodeOfConduct(self, pat_args, snapshot):
        """Test if a CODE_OF_CONDUCT file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @patch.object(
        CommunityStandardsQuery,
        "GetData",
        GetDataFunctional("CODE_OF_CONDUCT.md"),
    )
    def test_NoCodeOfConduct(self, pat_args, snapshot):
        """Test if a CODE_OF_CONDUCT file does not exist in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_CodeOwners(self, pat_args, snapshot):
        """Test if a CODEOWNERS file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @patch.object(
        CommunityStandardsQuery,
        "GetData",
        GetDataFunctional(".github/CODEOWNERS"),
    )
    def test_NoCodeOwners(self, pat_args, snapshot):
        """Test if a CODEOWNERS file does not exist in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_Contributing(self, pat_args, snapshot):
        """Test if a CONTRIBUTING.md file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @patch.object(
        CommunityStandardsQuery,
        "GetData",
        GetDataFunctional("CONTRIBUTING.md"),
    )
    def test_NoContributing(self, pat_args, snapshot):
        """Test if a CONTRIBUTING file does not exist in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_IssueTemplate(self, pat_args, snapshot):
        """Test if an Issue template file (e.g. ISSUE_TEMPLATE.md) exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )
        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @patch.object(
        CommunityStandardsQuery,
        "GetData",
        GetDataFunctional(".github/ISSUE_TEMPLATE", True),
    )
    def test_NoIssueTemplate(self, pat_args, snapshot):
        """Test if no Issue template file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_PullRequestTemplate(self, pat_args, snapshot):
        """
        Test if a Pull Request template file (e.g. PULL_REQUEST_TEMPLATE.md)
        exists in the repository.
        """
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @patch.object(
        CommunityStandardsQuery,
        "GetData",
        GetDataFunctional(".github/pull_request_template.md"),
    )
    def test_NoPullRequestTemplate(self, pat_args, snapshot):
        """Test if no Pull Request template file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
                "--CommunityStandards-SecurityPolicy-unrequired",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_SecurityPolicy(self, pat_args, snapshot):
        """Test if a Security policy file (e.g. SECURITY.md) exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
            ],
        )

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @patch.object(
        CommunityStandardsQuery,
        "GetData",
        GetDataFunctional("SECURITY.md"),
    )
    def test_NoSecurityPolicy(self, pat_args, snapshot):
        """Test if no Security policy file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--CommunityStandards-CodeOfConduct-unrequired",
                "--CommunityStandards-CodeOwners-unrequired",
                "--CommunityStandards-Contributing-unrequired",
                "--CommunityStandards-IssueTemplates-unrequired",
                "--CommunityStandards-LicenseFile-unrequired",
                "--CommunityStandards-PullRequestTemplate-unrequired",
                "--CommunityStandards-ReadMe-unrequired",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.fixture
def args() -> list[str]:
    return [
        "--include",
        "CommunityStandards",
        "--CommunityStandards-url",
        GetGithubUrl(),
    ]


# ----------------------------------------------------------------------
@pytest.fixture
def pat_args(args) -> list[str]:
    github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()
    CheckPATFileExists(github_pat_filename)

    return args + ["--CommunityStandards-pat", str(github_pat_filename)]
