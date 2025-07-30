# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for SecretScanningPushProtection.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.SecretScanningPushProtection import (
    SecretScanningPushProtection,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "security_and_analysis": {
                "secret_scanning_push_protection": {
                    "status": True,
                },
            },
        },
    }


@pytest.fixture
def requirement():
    return SecretScanningPushProtection()


class TestSecretScanningPushProtection:
    def test_security_and_analysis_missing(self, requirement, query_data):
        """Test if `security_and_analysis` is missing"""
        query_data["standard"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_secret_scanning_push_protection_missing(self, requirement, query_data):
        """Test if `secret_scanning_push_protection` is missing"""
        query_data["standard"]["security_and_analysis"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_status_missing(self, requirement, query_data):
        """Test if `status` is missing"""
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_status_none(self, requirement, query_data):
        """Test if `status` is None"""
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"]["status"] = None
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Incorrect(self, requirement, query_data):
        """Test when result doesn't match expected value"""
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"]["status"] = True
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "'Push protection' must be set to 'True' (it is currently set to 'False')." in result.context

    def test_Successful(self, requirement, query_data):
        """Successful"""
        query_data["standard"]["security_and_analysis"]["secret_scanning_push_protection"]["status"] = True
        requirement_args = {"disabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
