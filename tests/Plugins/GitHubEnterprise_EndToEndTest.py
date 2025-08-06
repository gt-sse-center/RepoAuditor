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


# ----------------------------------------------------------------------
class TestRulesets:
    """End-to-end tests for enabled/disabled rules within a ruleset in a GitHub repository."""

    def test_Default(self, pat_args, snapshot, monkeypatch):
        """Test for default case when no rulesets are present on the branch."""

        from RepoAuditor.Plugins.GitHub.RulesetQuery import RulesetQuery

        def MockGetData(
            self,
            module_data,
        ):
            """Mock version for GetData for RulesetQuery"""
            # Specify empty ruleset data as the default
            module_data["rules"] = []

            return module_data

        monkeypatch.setattr(RulesetQuery, "GetData", MockGetData)

        result = CliRunner().invoke(app, pat_args)

        # Error since no enabled rulesets
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RestrictCreationsRule(self, pat_args, snapshot):
        """Test for requirement `Restrict creation of the branch` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RestrictCreationsRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RestrictUpdatesRule(self, pat_args, snapshot):
        """Test for requirement `Restrict update of the branch` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RestrictUpdatesRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RestrictDeletionsRule(self, pat_args, snapshot):
        """Test for requirement `Restrict deletion of the branch` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RestrictDeletionsRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireLinearHistoryRule(self, pat_args, snapshot):
        """Test for requirement `Prevent merge commits on branch` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RequireLinearHistoryRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireSuccessfulDeploymentsRule(self, pat_args, snapshot):
        """Test for requirement `Require deployments to succeed` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RequireSuccessfulDeploymentsRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireSignedCommitsRule(self, pat_args, snapshot):
        """Test for requirement `Require signed commits` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireSignedCommitsRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequirePullRequestsRule(self, pat_args, snapshot):
        """Test for requirement `Require a pull request before merging` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequirePullRequestsRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireApprovalsRule(self, pat_args, snapshot):
        """Test for requirement `Require a pull request before merging -> Required approvals` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireApprovalsRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_DismissStalePullRequestApprovalsRule(self, pat_args, snapshot):
        """Test for requirement `Require a pull request before merging -> Dismiss stale pull request approvals when new commits are pushed` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-DismissStalePullRequestApprovalsRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireCodeOwnerReviewRule(self, pat_args, snapshot):
        """Test for requirement `Require a pull request before merging -> Require review from Code Owners` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-RequireCodeOwnerReviewRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireApprovalMostRecentPushRule(self, pat_args, snapshot):
        """Test for requirement `Require a pull request before merging -> Required approvals` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireApprovalMostRecentPushRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireConversationResolutionRule(self, pat_args, snapshot):
        """Test for requirement `Require a pull request before merging -> Required approvals` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireConversationResolutionRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireStatusChecksToPassRule(self, pat_args, snapshot):
        """Test for requirement `Require status checks to pass` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireStatusChecksToPassRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireUpToDateBranchesRule(self, pat_args, snapshot):
        """Test for requirement `Require status checks to pass -> Require branches to be up to date before merging` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireUpToDateBranchesRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    @pytest.mark.skip(reason="GitHub hosted runners not available on Enterprise")
    def test_EnsureStatusChecksRule(self, pat_args, snapshot):
        """Test for requirement `Require status checks to pass -> Status checks that are required` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-EnsureStatusChecksRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_AllowMainlineForcePushesRule(self, pat_args, snapshot):
        """Test for requirement `Block force pushes to the specified branch` is enabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-AllowMainlineForcePushesRule"])

        # Since the repo ruleset has the requirement disabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot

    def test_RequireCodeScanningResultsRule(self, pat_args, snapshot):
        """Test for requirement `Require code scanning results` is disabled in the ruleset for the `main` branch."""
        result = CliRunner().invoke(app, pat_args + ["--GitHub-no-RequireCodeScanningResultsRule"])

        # Since the repo ruleset has the requirement enabled,
        # we should get an error.
        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot
