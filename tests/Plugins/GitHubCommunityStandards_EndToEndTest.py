# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the GitHubCommunityStandards plugin."""

from pathlib import Path

import pytest
from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    InitializeStreamCapabilities,
)
from typer.testing import CliRunner
from utilities import CheckPATFileExists, GetGithubUrl, ScrubDurationGithuburlAndSpaces

from RepoAuditor.EntryPoint import app

# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


# ----------------------------------------------------------------------
class TestCommunityStandards:
    """End-to-end tests for community standards files in a GitHub repository."""

    # ----------------------------------------------------------------------
    def test_CodeOwners(self, pat_args, snapshot):
        """Test if a CODEOWNERS file exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCommunityStandards-CodeOwners-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_NoCodeOwners(self, pat_args, snapshot):
        """Test if a CODEOWNERS file does not exist in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHubCommunityStandards-CodeOwners-exists",
                "--GitHubCommunityStandards-branch",
                "test-GitHubCommunityStandards",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_Contributing(self, pat_args, snapshot):
        """Test if a CONTRIBUTING.md file exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCommunityStandards-Contributing-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_NoContributing(self, pat_args, snapshot):
        """Test if a CONTRIBUTING file does not exist in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHubCommunityStandards-Contributing-exists",
                "--GitHubCommunityStandards-branch",
                "test-GitHubCommunityStandards",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_IssueTemplate(self, pat_args, snapshot):
        """Test if an Issue template file (e.g. ISSUE_TEMPLATE.md) exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCommunityStandards-IssueTemplates-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_NoIssueTemplate(self, pat_args, snapshot):
        """Test if no Issue template file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHubCommunityStandards-IssueTemplates-exists",
                "--GitHubCommunityStandards-branch",
                "test-GitHubCommunityStandards",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_PullRequestTemplate(self, pat_args, snapshot):
        """Test if a Pull Request template file (e.g. PULL_REQUEST_TEMPLATE.md) exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCommunityStandards-PullRequestTemplate-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_NoPullRequestTemplate(self, pat_args, snapshot):
        """Test if no Pull Request template file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHubCommunityStandards-PullRequestTemplate-exists",
                "--GitHubCommunityStandards-branch",
                "test-GitHubCommunityStandards",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_SecurityPolicy(self, pat_args, snapshot):
        """Test if a Security policy file (e.g. SECURITY.md) exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCommunityStandards-SecurityPolicy-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_NoSecurityPolicy(self, pat_args, snapshot):
        """Test if no Security policy file exists in the repository."""
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHubCommunityStandards-SecurityPolicy-exists",
                "--GitHubCommunityStandards-branch",
                "test-GitHubCommunityStandards",
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
        "GitHubCommunityStandards",
        "--GitHubCommunityStandards-url",
        GetGithubUrl(),
    ]


# ----------------------------------------------------------------------
@pytest.fixture
def pat_args(args) -> list[str]:
    _github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()
    CheckPATFileExists(_github_pat_filename)

    with _github_pat_filename.open() as f:
        pat_value = f.read().strip()

    return args + ["--GitHubCommunityStandards-pat", pat_value]
