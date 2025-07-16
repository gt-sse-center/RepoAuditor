# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for RequireApprovals.py"""

import pytest

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireApprovals import RequireApprovals
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "branch": "main",
        "branch_protection_data": {
            "required_pull_request_reviews": {
                "required_approving_review_count": "1",
            },
        },
    }


@pytest.fixture
def requirement():
    return RequireApprovals()


@pytest.fixture(name="requirement_args")
def requirement_args_fixture():
    return {"value": "1"}


class TestRequireApprovals:
    def test_required_pull_request_reviews_missing(self, requirement, query_data, requirement_args):
        """Test when `required_pull_request_reviews` is missing"""
        query_data["branch_protection_data"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_required_pull_request_reviews_none(self, requirement, query_data, requirement_args):
        """Test when `required_pull_request_reviews` is None"""
        query_data["branch_protection_data"]["required_pull_request_reviews"] = None
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_required_approving_review_count_missing(self, requirement, query_data, requirement_args):
        """Test when `required_approving_review_count` is missing"""
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_required_approving_review_count_none(self, requirement, query_data, requirement_args):
        """Test when `required_approving_review_count` is None"""
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "required_approving_review_count"
        ] = None
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_IncorrectValue(self, requirement, query_data, requirement_args):
        """Test incorrect"""
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "required_approving_review_count"
        ] = "2"
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "'Require a pull request before merging -> Require approvals' must be set to '1' (it is currently set to '2')."
            in result.context
        )

    def test_Successful(self, requirement, query_data, requirement_args):
        """Test successful"""
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "required_approving_review_count"
        ] = "1"
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
