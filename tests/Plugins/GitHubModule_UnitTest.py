# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHub/Module.py"""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase as FakeFSTestCase

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.DismissStalePullRequestApprovals import (
    DismissStalePullRequestApprovals,
)
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.EnsureStatusChecks import (
    EnsureStatusChecks,
)
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicValueRequirementImpl import (
    ClassicValueRequirementImpl,
)
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireApprovalMostRecentPush import (
    RequireApprovalMostRecentPush,
)
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireApprovals import RequireApprovals
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireCodeOwnerReview import (
    RequireCodeOwnerReview,
)
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireUpToDateBranches import (
    RequireUpToDateBranches,
)
from RepoAuditor.Plugins.GitHub.DefaultBranchQueryRequirements.Protected import Protected
from RepoAuditor.Plugins.GitHub.Module import GitHubModule
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.DependabotSecurityUpdates import (
    DependabotSecurityUpdates,
)
from RepoAuditor.Plugins.GitHub.Impl.ValueRequirementImpl import ValueRequirementImpl, DoesNotApplyResult
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.Description import Description
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.License import License
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.MergeCommitMessage import MergeCommitMessage
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.Private import Private
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.SecretScanning import SecretScanning
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.SecretScanningPushProtection import (
    SecretScanningPushProtection,
)
from RepoAuditor.Plugins.GitHub.StandardQueryRequirements.SquashMergeCommitMessage import (
    SquashMergeCommitMessage,
)
from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession
from RepoAuditor.Requirement import EvaluateResult


class TestGitHubSession(FakeFSTestCase):
    """Unit tests for the _GitHubSession class."""

    def setUp(self):
        self.setUpPyfakefs()

    def test_Construct(self):
        """Test constructor."""
        github_url = "https://github.com/gt-sse-center/RepoAuditor"

        github_pat = Path(__file__).parent / "dummy_github_pat.txt"
        self.fs.create_file(github_pat, contents="github_path_abcdefghijklmnop")

        session = _GitHubSession(github_url=github_url, github_pat=github_pat)

        assert session.github_url == github_url

        # Test with trailing slash for URL
        session = _GitHubSession(github_url=github_url + "/", github_pat=github_pat)

        assert session.github_url == github_url

        # Test with invalid repository
        with pytest.raises(ValueError):
            session = _GitHubSession(
                github_url="https://github.com/gt-sse-center/RepoAuditor/123", github_pat=github_pat
            )

        # Test with enterprise URL
        github_enterprise_url = "https://github.gatech.edu/gt-sse-center/RepoAuditor"
        session = _GitHubSession(github_url=github_enterprise_url, github_pat=github_pat)
        assert session.github_url == github_enterprise_url


@pytest.fixture
def session():
    """Create a dummy GitHub API session object."""

    class _GithubSession_:
        pass

    s = _GithubSession_()
    s.github_url = "https://github.com/gt-sse-center/RepoAuditor"
    s.pat = "dummy_github_pat.txt"
    return s


class TestGitHubModule:
    """Unit tests for the Module class in the GitHub plugin."""

    def test_Construct(self):
        """Test constructor."""
        module = GitHubModule()
        assert isinstance(module, GitHubModule)

    def test_GenerateInitialData(self):
        """Test GenerateInitialData method."""
        dynamic_args = {
            "url": "https://github.com/gt-sse-center/RepoAuditor",
            "pat": Path(__file__).parent / "dummy_github_pat.txt",
        }
        module = GitHubModule()
        dynamic_args = module.GenerateInitialData(dynamic_args)

        assert "session" in dynamic_args
        assert isinstance(dynamic_args["session"], _GitHubSession)

    def test_ValueRequirementImpl(self):
        """Test the ValueRequirementImpl class."""

        requirement = ValueRequirementImpl(
            "TestValueRequirement",
            "42",
            "Test Value Requirement",
            lambda data: data.get("result", None),
            "",
            "",
        )

        requirement_1 = ValueRequirementImpl(
            "TestValueRequirement",
            "42",
            "Test Value Requirement",
            lambda data: data.get("result", None),
            "",
            "",
            missing_value_is_warning=False,
        )

        requirement_2 = ValueRequirementImpl(
            "TestValueRequirement",
            "42",
            None,
            lambda data: DoesNotApplyResult(""),
            "",
            "",
        )

        # Test pathway where result value is None
        query_data = {"result": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data" in result.context

        query_data = {"result": None}
        requirement_args = {}
        result = requirement_1.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        query_data = {"result": None}
        requirement_args = {}

        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data" in result.context

        # Test pathway where expected value is default
        query_data = {"result": "43"}
        requirement_args = {"value": "42"}
        result = requirement_2.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply

        # Test pathway where result is DoesNotApplyResult
        query_data = {"result": "42"}
        requirement_args = {"value": "43"}
        result = requirement_2.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "the entity cannot be set to '43' because " in result.context

        # Test pathway where result value and expected value don't match
        query_data = {"result": "43"}
        requirement_args = {"value": "40"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "'Test Value Requirement' must be set to '40' (it is currently set to '43')." in result.context

        # Test successful
        query_data = {"result": "42"}
        requirement_args = {"value": "42"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test successful with GetDynamicArgDefinitions
        query_data = {"result": "42"}
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success


class TestClassicBranchProtectionRequirements:
    def test_ClassicValueRequirementImpl(self):
        """Test the ClassicValueRequirementImpl class."""
        requirement = ClassicValueRequirementImpl(
            "Require Some Value",
            "Disabled",
            github_settings_section=None,
            github_settings_value="No Settings Section",
            get_configuration_value_func=lambda _: "yes",
            rationale="For testing",
        )
        assert requirement.github_settings_value == "'No Settings Section'"

        requirement = ClassicValueRequirementImpl(
            "Require Some Value",
            "Disabled",
            github_settings_section="Protect funky feature",
            github_settings_value=None,
            get_configuration_value_func=lambda _: "yes",
            rationale="For testing",
        )
        assert requirement.github_settings_value == "the entity"

    def test_EnsureStatusChecks(self, session):
        """Test the EnsureStatusChecks requirement."""
        requirement = EnsureStatusChecks()

        # Test disabled requirement
        query_data = {
            "session": session,
            "branch": "main",
        }
        requirement_args = {"disable": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "The status check requirement has been explicitly disabled." in result.context

        # Test when `required_status_checks` is missing
        query_data["branch_protection_data"] = {}
        requirement_args = {"disable": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_status_checks` is None
        query_data["branch_protection_data"] = {"required_status_checks": None}
        requirement_args = {"disable": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `checks` is missing
        query_data["branch_protection_data"]["required_status_checks"] = {}
        requirement_args = {"disable": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "No status checks are configured." in result.context

        # Test when `checks` is None
        query_data["branch_protection_data"]["required_status_checks"] = {"checks": None}
        requirement_args = {"disable": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "No status checks are configured." in result.context

        # Test successful
        query_data["branch_protection_data"]["required_status_checks"]["checks"] = ["check1", "check2"]
        requirement_args = {"disable": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test with GetDynamicArgDefinitions
        query_data["branch_protection_data"]["required_status_checks"]["checks"] = ["check1", "check2"]
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_DismissStalePullRequestApprovals(self, session):
        """Test the DismissStalePullRequestApprovals requirement."""
        requirement = DismissStalePullRequestApprovals()

        # Test disabled requirement
        query_data = {
            "session": session,
            "branch": "main",
        }

        # Test when `required_pull_request_reviews` is missing
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_pull_request_reviews` is None
        query_data["branch_protection_data"] = {"required_pull_request_reviews": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `dismiss_stale_reviews` is missing
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `dismiss_stale_reviews` is None
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {
            "dismiss_stale_reviews": None
        }
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test successful
        query_data["branch_protection_data"]["required_pull_request_reviews"]["dismiss_stale_reviews"] = True
        requirement_args["false"] = False
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_RequireApprovalMostRecentPush(self, session):
        """Test the RequireApprovalMostRecentPush requirement."""
        requirement = RequireApprovalMostRecentPush()

        # Test disabled requirement
        query_data = {
            "session": session,
            "branch": "main",
        }

        # Test when `required_pull_request_reviews` is missing
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_pull_request_reviews` is None
        query_data["branch_protection_data"] = {"required_pull_request_reviews": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `require_last_push_approval` is missing
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `require_last_push_approval` is None
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {
            "require_last_push_approval": None
        }
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test successful
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "require_last_push_approval"
        ] = True
        requirement_args["false"] = False
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_RequireApprovals(self, session):
        """Test the RequireApprovals requirement."""
        requirement = RequireApprovals()

        # Test disabled requirement
        query_data = {
            "session": session,
            "branch": "main",
        }

        # Test when `required_pull_request_reviews` is missing
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_pull_request_reviews` is None
        query_data["branch_protection_data"] = {"required_pull_request_reviews": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_approving_review_count` is missing
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_approving_review_count` is None
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {
            "required_approving_review_count": None
        }
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test incorrect
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "required_approving_review_count"
        ] = "2"
        requirement_args["value"] = "1"
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "'Require a pull request before merging -> Require approvals' must be set to '1' (it is currently set to '2')."
            in result.context
        )

        # Test successful
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "required_approving_review_count"
        ] = "1"
        requirement_args["value"] = "1"
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_RequireCodeOwnerReview(sel, session):
        """Test the RequireCodeOwnerReview requirement."""
        requirement = RequireCodeOwnerReview()

        # Test disabled requirement
        query_data = {
            "session": session,
            "branch": "main",
        }

        # Test when `required_pull_request_reviews` is missing
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_pull_request_reviews` is None
        query_data["branch_protection_data"] = {"required_pull_request_reviews": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `require_code_owner_reviews` is missing
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `require_code_owner_reviews` is None
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {
            "require_code_owner_reviews": None
        }
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test incorrect
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "require_code_owner_reviews"
        ] = False
        requirement_args["true"] = True
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "Require a pull request before merging -> Require review from Code Owners' must be set to 'True' (it is currently set to 'False')."
            in result.context
        )

        # Test successful
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "require_code_owner_reviews"
        ] = True
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_RequireUpToDateBranches(self, session):
        """Test the RequireUpToDateBranches requirement."""
        requirement = RequireUpToDateBranches()

        # Test disabled requirement
        query_data = {
            "session": session,
            "branch": "main",
        }

        # Test when `required_status_checks` is missing
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `required_status_checks` is None
        query_data["branch_protection_data"] = {"required_status_checks": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `strict` is missing
        query_data["branch_protection_data"]["required_status_checks"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test when `strict` is None
        query_data["branch_protection_data"]["required_status_checks"] = {"strict": None}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

        # Test incorrect
        query_data["branch_protection_data"]["required_status_checks"]["strict"] = False
        requirement_args["false"] = False
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "'Require status checks to pass before merging -> Require branches to be up to date before merging' must be set to 'True' (it is currently set to 'False')."
            in result.context
        )

        # Test successful
        query_data["branch_protection_data"]["required_status_checks"]["strict"] = False
        requirement_args["false"] = True
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success


class TestDefaultBranchQueryRequirements:
    def test_Protected(self, session):
        """Test the Protected requirement."""
        requirement = Protected()

        # Test for incomplete result
        query_data = {
            "default_branch_data": {},
            "session": session,
        }
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)

        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        query_data["default_branch_data"] = {"protected": True}
        # Don't protect mainline branch
        requirement_args = {"false": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert result.rationale is None
        assert result.resolution is not None

        # Protect mainline branch
        requirement_args = {"false": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
        assert result.rationale is None
        assert result.resolution is None

        # is_protected is False
        query_data["default_branch_data"]["protected"] = False
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert result.rationale is not None
        assert result.resolution is not None


class TestStandardQueryRequirements:
    def test_License(self):
        """Test the License value requirement."""
        requirement = License()

        # Check if no "license" key in query_data
        # We should get a `IncompleteDataResult`.
        result = requirement.Evaluate(
            query_data={"standard": {}},
            requirement_args={},
        )
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Check if no data under key "license",
        # in which case the license value is returned as the empty string.
        result = requirement.Evaluate(
            query_data={"standard": {"license": None}},
            requirement_args={"value": requirement.default_value},
        )
        assert result.result == EvaluateResult.Error
        assert "the entity must be set to 'MIT License' (it is currently set to '')." in result.context

    def test_MergeCommitMessage(self, session):
        """Test MergeCommitMessage requirement."""
        requirement = MergeCommitMessage()

        query_data = {
            "session": session,
        }

        # Test if `allow_merge_commit` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `allow_merge_commit` is None
        query_data["standard"] = {"allow_merge_commit": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test when merge commits are disabled
        query_data["standard"] = {"allow_merge_commit": False}
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "Merge commits are not enabled" in result.context

        # Missing merge_commit_message value
        query_data["standard"] = {"allow_merge_commit": True}
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # With BLANK commit message value
        query_data["standard"]["merge_commit_message"] = "BLANK"
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # With incorrect commit message value
        query_data["standard"]["merge_commit_message"] = "BLUR"
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "it is currently set to 'BLUR'" in result.context

    def test_Description(self, session):
        """Test Description requirement."""
        requirement = Description()

        query_data = {
            "session": session,
        }

        # Test if `description` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `description` is None
        query_data["standard"] = {"description": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test when description is not allowed to be empty
        query_data["standard"]["description"] = ""
        requirement_args = {"allow-empty": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's description must be not be empty." in result.context

        # Test when description is allowed to be empty
        query_data["standard"]["description"] = ""
        requirement_args = {"allow-empty": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test using GetDynamicArgDefinitions
        query_data["standard"]["description"] = "Description of repository"
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_Private(self, session):
        """Test Private requirement."""
        requirement = Private()

        query_data = {
            "session": session,
        }

        # Test if `private` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `private` is None
        query_data["standard"] = {"private": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test when repository is expected to be public.
        query_data["standard"]["private"] = ""
        requirement_args = {"true": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's visibility must be public." in result.context

        # Test when repository is expected to be private.
        query_data["standard"]["private"] = ""
        requirement_args = {"true": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's visibility must be private." in result.context

        # Test when repository is private
        query_data["standard"]["private"] = True
        requirement_args = {"true": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test when repository is public
        query_data["standard"]["private"] = False
        requirement_args = {"true": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test using GetDynamicArgDefinitions
        query_data["standard"]["private"] = False
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_SquashMergeCommitMessage(self, session):
        """Test SquashMergeCommitMessage requirement."""
        requirement = SquashMergeCommitMessage()

        query_data = {
            "session": session,
        }

        # Test if `allow_merge_commit` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `allow_merge_commit` is None
        query_data["standard"] = {"allow_merge_commit": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test when squash merges are disabled
        query_data["standard"] = {"allow_squash_merge": False}
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "Squash merge commits are not enabled." in result.context

        # Missing squash_merge_commit_message value
        query_data["standard"] = {"allow_squash_merge": True}
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # With COMMIT_MESSAGES squash-merge commit message value
        query_data["standard"]["squash_merge_commit_message"] = "COMMIT_MESSAGES"
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # With incorrect commit message value
        query_data["standard"]["squash_merge_commit_message"] = "NO_COMMIT_MESSAGES"
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "it is currently set to 'NO_COMMIT_MESSAGES'" in result.context

    def test_DependabotSecurityUpdates(self, session):
        """Test DependabotSecurityUpdates requirement."""
        requirement = DependabotSecurityUpdates()

        query_data = {
            "session": session,
        }

        # Test if `security_and_analysis` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `dependabot_security_updates` is missing
        query_data["standard"]["security_and_analysis"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `status` is missing
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `status` is None
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"] = {"status": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Result doesn't match expected value
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"]["status"] = True
        requirement_args = {"false": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "'Dependabot security updates' must be set to 'True' (it is currently set to 'False')."
            in result.context
        )

        # Successful
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"]["status"] = True
        requirement_args = {"false": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_SecretScanning(self, session):
        """Test SecretScanning requirement."""
        requirement = SecretScanning()

        query_data = {
            "session": session,
        }

        # Test if `security_and_analysis` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `dependabot_security_updates` is missing
        query_data["standard"]["security_and_analysis"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `dependabot_security_updates` is None
        query_data["standard"]["security_and_analysis"] = {"dependabot_security_updates": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `status` is missing
        query_data["standard"]["security_and_analysis"]["secret_scanning"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `status` is None
        query_data["standard"]["security_and_analysis"]["secret_scanning"] = {"status": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Result doesn't match expected value
        query_data["standard"]["security_and_analysis"]["secret_scanning"]["status"] = True
        requirement_args = {"false": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "'Secret protection' must be set to 'True' (it is currently set to 'False')." in result.context

        # Successful
        query_data["standard"]["security_and_analysis"]["secret_scanning"]["status"] = True
        requirement_args = {"false": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_SecretScanningPushProtection(self, session):
        """Test SecretScanningPushProtection requirement."""
        requirement = SecretScanningPushProtection()

        query_data = {
            "session": session,
        }

        # Test if `security_and_analysis` is missing
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `dependabot_security_updates` is missing
        query_data["standard"]["security_and_analysis"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `dependabot_security_updates` is None
        query_data["standard"]["security_and_analysis"] = {"dependabot_security_updates": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `status` is missing
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"] = {}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Test if `status` is None
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"] = {"status": None}
        result = requirement.Evaluate(query_data, requirement_args={})
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

        # Result doesn't match expected value
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"]["status"] = True
        requirement_args = {"false": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "'Push protection' must be set to 'True' (it is currently set to 'False')." in result.context

        # Successful
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"]["status"] = True
        requirement_args = {"false": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
