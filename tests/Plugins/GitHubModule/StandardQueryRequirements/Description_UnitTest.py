# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for Description.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.Description import Description
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "description": "Description of repository",
        },
    }


@pytest.fixture
def requirement():
    return Description()


class TestDescription:
    """Unit tests for the Description requirement."""

    def test_description_missing(self, requirement, query_data):
        """Test if `description` is missing.
        This happens if no `description` key is present in API response.
        """
        query_data["standard"] = {}
        requirement_args = {"allow-empty": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's description must be not be empty." in result.context

    def test_description_none(self, requirement, query_data):
        """Test if `description` is None."""
        query_data["standard"]["description"] = None
        requirement_args = {"allow-empty": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's description must be not be empty." in result.context

    def test_NotAllowEmpty(self, requirement, query_data):
        """Test when description is not allowed to be empty"""
        query_data["standard"]["description"] = ""
        requirement_args = {"allow-empty": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "The repository's description must be not be empty." in result.context

    def test_AllowEmpty(self, requirement, query_data):
        """Test when description is allowed to be empty"""
        query_data["standard"]["description"] = ""
        requirement_args = {"allow-empty": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_SuccessfulGetDynamicArgDefinitions(self, requirement, query_data):
        """Test using GetDynamicArgDefinitions"""
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
