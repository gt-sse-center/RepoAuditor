# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for Private.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.Private import Private
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "private": True,
        },
    }


@pytest.fixture
def requirement():
    return Private()


class TestPrivate:
    def test_private_missing(self, requirement, query_data):
        """Test if `private` is missing"""
        query_data["standard"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_private_none(self, requirement, query_data):
        """Test if `private` is None"""
        query_data["standard"]["private"] = None
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_PublicRepo(self, requirement, query_data):
        """Test when repository is expected to be public."""
        query_data["standard"]["private"] = True
        requirement_args = {"enabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's visibility must be public." in result.context

    def test_Incorrect(self, requirement, query_data):
        """Test when repository is expected to be private but is actually not."""
        query_data["standard"]["private"] = False
        requirement_args = {"enabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's visibility must be private." in result.context

    def test_Successful(self, requirement, query_data):
        """Test when repository is private"""
        query_data["standard"]["private"] = True
        requirement_args = {"enabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test when repository is public
        query_data["standard"]["private"] = False
        requirement_args = {"enabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

        # Test using GetDynamicArgDefinitions
        query_data["standard"]["private"] = False
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
