# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the GitHubCustomization plugin."""

import pytest
from pathlib import Path

from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    InitializeStreamCapabilities,
)
from typer.testing import CliRunner

from RepoAuditor.EntryPoint import app

from utilities import ScrubDurationGithuburlAndSpaces, GetGithubUrl, CheckPATFileExists

# ----------------------------------------------------------------------
_github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()
CheckPATFileExists(_github_pat_filename)

# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


# ----------------------------------------------------------------------
class TestCustomization:
    """End-to-end tests for customization files in a GitHub repository."""

    # ----------------------------------------------------------------------
    def test_CodeOwners(self, pat_args, snapshot):
        """Test if a CODEOWNERS file exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCustomization-CodeOwners-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_NoCodeOwners(self, pat_args, snapshot):
        """Test if a CODEOWNERS file does not exist in the repository."""
        # TODO: How to test if CodeOwners file doesn't exist without updating repo?
        result = CliRunner().invoke(app, pat_args)

        assert result.exit_code == 0, result.output
        # assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_Contributing(self, pat_args, snapshot):
        """Test if a CONTRIBUTING.md file exists in the repository."""
        result = CliRunner().invoke(app, pat_args + ["--GitHubCustomization-Contributing-exists"])

        assert result.exit_code == 0, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.fixture
def args() -> list[str]:
    return [
        "--include",
        "GitHubCustomization",
        "--GitHubCustomization-url",
        GetGithubUrl(),
    ]


# ----------------------------------------------------------------------
@pytest.fixture
def pat_args(args) -> list[str]:
    with _github_pat_filename.open() as f:
        pat_value = f.read().strip()

    return args + ["--GitHubCustomization-pat", pat_value]
