# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the plugins on an enterprise URL"""

import urllib
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
@pytest.fixture(name="args")
def args_fixture() -> list[str]:
    return [
        "--include",
        "GitHub",
        "--GitHub-url",
        GetGithubUrl("enterprise"),
        # Currently GitHub Enterprise does not support GitHub hosted runners.
        # As a result, no status checks show up to select and this will always fail.
        "--GitHub-no-EnsureStatusChecks",
    ]


# ----------------------------------------------------------------------
@pytest.fixture(name="pat_args")
def pat_args_fixture(args) -> list[str]:
    github_pat_filename = (Path(__file__).parent / "github_gatech_pat.txt").resolve()
    parsed = urllib.parse.urlparse(GetGithubUrl("enterprise"))
    parsed = parsed._replace(path="")
    CheckPATFileExists(github_pat_filename, github_url=parsed.geturl())

    return args + ["--GitHub-pat", str(github_pat_filename)]


# ----------------------------------------------------------------------
def test_Successful(pat_args, snapshot):
    """Test if RepoAuditor runs successfully with default options."""
    result = CliRunner().invoke(app, pat_args)

    assert result.exit_code == 0, result.output
    assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot


# ----------------------------------------------------------------------
class TestStandard:
    # ----------------------------------------------------------------------
    def test_NoAutoMerge(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-AutoMerge"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoDeleteHeadBranches(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-DeleteHeadBranches"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    @pytest.mark.skip(reason="Not enabled by Enterprise Administrator")
    def test_NoDependabotSecurityUpdates(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-DependabotSecurityUpdates"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoMergeCommit(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-MergeCommit"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesRebaseMergeCommit(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RebaseMergeCommit"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    @pytest.mark.skip(reason="Not enabled by Enterprise Administrator")
    def test_NoSecretScanning(self, pat_args, snapshot):
        """Test is secret scanning is not disabled."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-SecretScanning"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    @pytest.mark.skip(reason="Not enabled by Enterprise Administrator")
    def test_NoSecretScanningPushProtection(self, pat_args, snapshot):
        """Test is secret scanning push protection is not disabled."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-SecretScanningPushProtection"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesSquashCommitMerge(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SquashCommitMerge"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesSuggestUpdatingPullRequestBranches(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SuggestUpdatingPullRequestBranches"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesSupportDiscussions(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SupportDiscussions"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSupportIssues(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-SupportIssues"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSupportProjects(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-SupportProjects"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSupportWikis(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-SupportWikis"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesTemplateRepository(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-TemplateRepository"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoWebCommitSignoff(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-WebCommitSignoff"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_DefaultBranchValue(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-DefaultBranch-value", "not_main"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_LicenseValue(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-License-value", "Not the MIT License"])

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_MergeCommitMessageValue(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHub-MergeCommitMessage-value",
                "This is not a valid merge commit message",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_PrivateValue(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-Private"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_SquashMergeCommitMessageValue(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args
            + [
                "--GitHub-SquashMergeCommitMessage-value",
                "This is not a valid squash merge commit message",
            ],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_Protected(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-Protected"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot


# ----------------------------------------------------------------------
class TestClassic:
    # ----------------------------------------------------------------------
    def test_AllowDeletions(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-AllowDeletions"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_AllowForcePush(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-AllowMainlineForcePushes"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_DismissStalePullRequestApprovals(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-DismissStalePullRequestApprovals"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_DoNotAllowBypassSettings(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-DoNotAllowBypassSettings"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    @pytest.mark.skip(reason="GitHub hosted runners not available on Enterprise")
    def test_EnsureStatusChecks(self, pat_args):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-EnsureStatusChecks-disable", "--verbose"],
        )

        assert result.exit_code == 0, result.output
        assert "[DoesNotApply] EnsureStatusChecks" in result.stdout

    # ----------------------------------------------------------------------
    def test_RequireApprovalMostRecentPush(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-RequireApprovalMostRecentPush"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireApprovals(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireApprovals-value", "2"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireCodeOwnerReview(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireCodeOwnerReview"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireConversationResolution(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-RequireConversationResolution"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireLinearHistory(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireLinearHistory"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequirePullRequests(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-RequirePullRequests"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireSignedCommits(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-RequireSignedCommits"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireStatusChecksToPass(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-RequireStatusChecksToPass"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireUpToDateBranches(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-no-RequireUpToDateBranches"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot
