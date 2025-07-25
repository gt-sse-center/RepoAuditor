import pytest

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireUpToDateBranches import (
    RequireUpToDateBranches,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "branch": "main",
        "branch_protection_data": {
            "required_status_checks": {
                "strict": False,
            },
        },
    }


@pytest.fixture
def requirement():
    return RequireUpToDateBranches()


class TestRequireUpToDateBranches:
    def test_required_status_checks_missing(self, requirement, query_data):
        """Test when `required_status_checks` is missing"""
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_required_status_checks_none(self, requirement, query_data):
        """Test when `required_status_checks` is None"""
        query_data["branch_protection_data"] = {"required_status_checks": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_strict_missing(self, requirement, query_data):
        """Test when `strict` is missing"""
        query_data["branch_protection_data"]["required_status_checks"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_strict_none(self, requirement, query_data):
        """Test when `strict` is None"""
        query_data["branch_protection_data"]["required_status_checks"] = {"strict": None}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_IncorrectValue(self, requirement, query_data):
        """Test incorrect"""
        query_data["branch_protection_data"]["required_status_checks"]["strict"] = False
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "'Require status checks to pass before merging -> Require branches to be up to date before merging' must be set to 'True' (it is currently set to 'False')."
            in result.context
        )

    def test_Successful(self, requirement, query_data):
        """Test successful"""
        query_data["branch_protection_data"]["required_status_checks"]["strict"] = False
        requirement_args = {"disabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
