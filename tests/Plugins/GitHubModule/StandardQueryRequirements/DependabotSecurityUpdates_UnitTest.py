# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for DependabotSecurityUpdates.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.DependabotSecurityUpdates import (
    DependabotSecurityUpdates,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "security_and_analysis": {
                "dependabot_security_updates": {
                    "status": True,
                },
            },
        },
    }


@pytest.fixture
def requirement():
    return DependabotSecurityUpdates()


class TestDependabotSecurityUpdates:
    def test_security_and_analysis_missing(self, requirement, query_data):
        """Test if `security_and_analysis` is missing"""
        query_data["standard"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_dependabot_security_updates_missing(self, requirement, query_data):
        """Test if `dependabot_security_updates` is missing"""
        query_data["standard"]["security_and_analysis"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_status_missing(self, requirement, query_data):
        """Test if `status` is missing"""
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_status_none(self, requirement, query_data):
        """Test if `status` is None"""
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"]["status"] = None
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Incorrect(self, requirement, query_data):
        """Result doesn't match expected value"""
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"]["status"] = True
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert (
            "'Dependabot security updates' must be set to 'True' (it is currently set to 'False')."
            in result.context
        )

    def test_Successful(self, requirement, query_data):
        """Successful"""
        query_data["standard"]["security_and_analysis"]["dependabot_security_updates"]["status"] = True
        requirement_args = {"disabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
