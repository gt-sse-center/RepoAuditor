# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the GitHub plugin"""

import os
import sys
import textwrap

from pathlib import Path

import pytest

from dbrownell_Common.Streams.Capabilities import Capabilities
from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    InitializeStreamCapabilities,
    ScrubDuration,
)
from typer.testing import CliRunner

from RepoAuditor.EntryPoint import app

# ----------------------------------------------------------------------
_github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()

if not _github_pat_filename.is_file():
    sys.stdout.write(
        textwrap.dedent(
            f"""\


            The filename '{_github_pat_filename}' does not exist. Please create this file and add your GitHub Personal Access Token (PAT) to it.
            This git repository is configured to ignore the file so that it will never be included as part of a commit.

            To create a new token:

                1. Visit https://github.com/settings/tokens/new
                2. Ensure that 'repo' scope is checked
                3. Click 'Generate token'
                4. Copy the token to the clipboard
                5. Create the file '{_github_pat_filename}'
                6. Paste the token into the created file
                7. Save the file and run these tests again.

            These tests query a repository on GitHub, but GitHub limits the number of concurrent requests made to a repository when a PAT is
            not provided. As a result, the tests will fail once the limit is reached.
            """,
        ),
    )

    sys.exit(-1)


# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


# ----------------------------------------------------------------------
def test_Successful(pat_args, snapshot):
    result = CliRunner().invoke(app, pat_args)

    assert result.exit_code == 0, result.output
    assert ScrubDuration(result.stdout) == snapshot


# ----------------------------------------------------------------------
def _skip_test_NoPAT():
    operating_system = os.getenv("GITHUB_CI_OPERATING_SYSTEM")
    python_version = os.getenv("GITHUB_CI_PYTHON_VERSION")

    if operating_system is None or python_version is None:
        # Always run locally
        return False

    # The selection of these values is arbitrary and serve only to ensure that the test is run on
    # one configuration.
    return operating_system != "ubuntu-latest" or python_version != "3.12"


@pytest.mark.skipif(
    _skip_test_NoPAT(),
    reason="Only run this test on the CI machine in specific configurations to avoid GitHub's request throttling.",
)
def test_NoPAT(snapshot, args):
    result = CliRunner().invoke(app, args)

    assert result.exit_code == 1, result.output
    assert ScrubDuration(result.stdout) == snapshot


# ----------------------------------------------------------------------
class TestStandard:
    # ----------------------------------------------------------------------
    def test_NoAutoMerge(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-AutoMerge-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoDeleteHeadBranches(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-DeleteHeadBranches-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoDependabotSecurityUpdates(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-DependabotSecurityUpdates-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoMergeCommit(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-MergeCommit-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesRebaseMergeCommit(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RebaseMergeCommit-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSecretScanning(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SecretScanning-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSecretScanningPushProtection(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SecretScanningPushProtection-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesSquashCommitMerge(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SquashCommitMerge-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesSuggestUpdatingPullRequestBranches(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app, pat_args + ["--GitHub-SuggestUpdatingPullRequestBranches-true"]
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesSupportDiscussions(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SupportDiscussions-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSupportIssues(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SupportIssues-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSupportProjects(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SupportProjects-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoSupportWikis(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-SupportWikis-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_YesTemplateRepository(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-TemplateRepository-true"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_NoWebCommitSignoff(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-WebCommitSignoff-false"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_DefaultBranchValue(self, pat_args, snapshot):
        result = CliRunner().invoke(app, pat_args + ["--GitHub-DefaultBranch-value", "not_main"])

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_LicenseValue(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app, pat_args + ["--GitHub-License-value", "Not the MIT License"]
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

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
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_PrivateValue(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-Private-true"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

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
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_Protected(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-Protected-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot


# ----------------------------------------------------------------------
class TestClassic:
    # ----------------------------------------------------------------------
    def test_AllowDeletions(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-AllowDeletions-true"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_AllowForcePush(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-AllowForcePushes-true"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_DismissStalePullRequestApprovals(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-DismissStalePullRequestApprovals-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_DoNotAllowBypassSettings(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-DoNotAllowBypassSettings-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
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
            pat_args + ["--GitHub-RequireApprovalMostRecentPush-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireApprovals(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireApprovals-value", "2"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireCodeOwnerReview(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireCodeOwnerReview-true"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireConversationResolution(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireConversationResolution-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireLinearHistory(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireLinearHistory-true"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequirePullRequests(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequirePullRequests-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireSignedCommits(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireSignedCommits-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireStatusChecksToPass(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireStatusChecksToPass-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot

    # ----------------------------------------------------------------------
    def test_RequireUpToDateBranches(self, pat_args, snapshot):
        result = CliRunner().invoke(
            app,
            pat_args + ["--GitHub-RequireUpToDateBranches-false"],
        )

        assert result.exit_code == -1, result.output
        assert ScrubDuration(result.stdout) == snapshot


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@pytest.fixture
def args() -> list[str]:
    return [
        "--include",
        "GitHub",
        "--GitHub-url",
        "https://github.com/gt-sse-center/RepoAuditor",
    ]


# ----------------------------------------------------------------------
@pytest.fixture
def pat_args(args) -> list[str]:
    with _github_pat_filename.open() as f:
        pat_value = f.read().strip()

    return args + ["--GitHub-pat", pat_value]
