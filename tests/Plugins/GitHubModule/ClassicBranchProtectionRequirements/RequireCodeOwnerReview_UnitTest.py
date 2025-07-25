# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for RequireCodeOwnerReview.py"""

import pytest

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.RequireCodeOwnerReview import (
    RequireCodeOwnerReview,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "branch": "main",
        "branch_protection_data": {
            "required_pull_request_reviews": {
                "require_code_owner_reviews": False,
            },
        },
    }


@pytest.fixture
def requirement():
    return RequireCodeOwnerReview()


class TestRequireCodeOwnerReview:
    def test_required_pull_request_reviews_missing(self, requirement, query_data):
        """Test when `required_pull_request_reviews` is missing"""
        query_data["branch_protection_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_required_pull_request_reviews_none(self, requirement, query_data):
        """Test when `required_pull_request_reviews` is None"""
        query_data["branch_protection_data"]["required_pull_request_reviews"] = None
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_require_code_owner_reviews_missing(self, requirement, query_data):
        """Test when `require_code_owner_reviews` is missing"""
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_require_code_owner_reviews_none(self, requirement, query_data):
        """Test when `require_code_owner_reviews` is None"""
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "require_code_owner_reviews"
        ] = None
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_IncorrectValue(self, requirement, query_data):
        """Test incorrect"""
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "require_code_owner_reviews"
        ] = False
        requirement_args = {"enabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "Require a pull request before merging -> Require review from Code Owners' must be set to 'True' (it is currently set to 'False')."
            in result.context
        )

    def test_Successful(self, requirement, query_data):
        """Test successful"""
        query_data["branch_protection_data"]["required_pull_request_reviews"][
            "require_code_owner_reviews"
        ] = True
        requirement_args = {"enabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
