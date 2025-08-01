# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for Protected.py"""

import pytest

from RepoAuditor.Plugins.GitHub.DefaultBranchRequirements.Protected import Protected
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture(name="query_data")
def query_data_fixture(session):
    return {
        "session": session,
        "default_branch_data": {
            "protected": True,
        },
    }


@pytest.fixture(name="requirement")
def requirement_fixture():
    return Protected()


class TestProtected:
    """Tests for the Protected requirement class."""

    def test_Incomplete(self, requirement, query_data):
        """Test for incomplete result"""
        query_data["default_branch_data"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_UnprotectedMainlineBranch(self, requirement, query_data):
        """Test for unprotected mainline branch."""
        query_data["default_branch_data"] = {"protected": True}
        # Don't protect mainline branch
        requirement_args = {"no": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert result.rationale is None
        assert result.resolution is not None

    def test_ProtectedMainlineBranch(self, requirement, query_data):
        """Test for protected mainline branch"""
        requirement_args = {"no": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
        assert result.rationale is None
        assert result.resolution is None

    def test_is_protected_False(self, requirement, query_data):
        """Test when is_protected is False"""
        query_data["default_branch_data"]["protected"] = False
        requirement_args = {"no": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert result.rationale is not None
        assert result.resolution is not None
