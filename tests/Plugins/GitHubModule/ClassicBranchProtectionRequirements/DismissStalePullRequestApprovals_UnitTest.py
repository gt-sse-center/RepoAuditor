# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for DismissStalePullRequestApprovals.py"""

import pytest

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.DismissStalePullRequestApprovals import (
    DismissStalePullRequestApprovals,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "branch": "main",
        "branch_protection_data": {
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
            },
        },
    }


@pytest.fixture
def requirement():
    return DismissStalePullRequestApprovals()


class TestDismissStalePullRequestApprovals:
    def test_required_pull_request_reviews_missing(self, requirement, query_data):
        """Test when `required_pull_request_reviews` is missing."""
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

    def test_dismiss_stale_reviews_missing(self, requirement, query_data):
        """Test when `dismiss_stale_reviews` is missing"""
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_dismiss_stale_reviews_none(self, requirement, query_data):
        """Test when `dismiss_stale_reviews` is None"""
        query_data["branch_protection_data"]["required_pull_request_reviews"] = {
            "dismiss_stale_reviews": None
        }
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_successful(self, requirement, query_data):
        """Test successful"""
        query_data["branch_protection_data"]["required_pull_request_reviews"]["dismiss_stale_reviews"] = True
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
