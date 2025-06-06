# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the GitHubRulesets plugin."""

from pathlib import Path
import pytest

from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    InitializeStreamCapabilities,
)
from typer.testing import CliRunner

from RepoAuditor.EntryPoint import app

from utilities import ScrubDurationGithuburlAndSpaces, GetGithubUrl, CheckPATFileExists

# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


# ----------------------------------------------------------------------
class TestGitHubRuleset:
    """End-to-end tests for rulesets in a GitHub repository."""

    def test_RequireStatusChecks(self, pat_args, snapshot):
        """Test for Status Checks not required ruleset"""
        result = CliRunner().invoke(app, pat_args + ["--GitHubRulesets-RequireStatusChecks-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequirePullRequests(self, pat_args, snapshot):
        """Test for Pull Requests required ruleset"""
        result = CliRunner().invoke(app, pat_args + ["--GitHubRulesets-RequirePullRequests-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireSignedCommits(self, pat_args, snapshot):
        """Test for Signed Commits required ruleset"""
        result = CliRunner().invoke(app, pat_args + ["--GitHubRulesets-RequireSignedCommits-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.fixture
def args() -> list[str]:
    return [
        "--include",
        "GitHubRulesets",
        "--GitHubRulesets-url",
        GetGithubUrl(),
    ]


# ----------------------------------------------------------------------
@pytest.fixture
def pat_args(args) -> list[str]:
    _github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()
    CheckPATFileExists(_github_pat_filename)

    with _github_pat_filename.open() as f:
        pat_value = f.read().strip()

    return args + ["--GitHubRulesets-pat", pat_value]
