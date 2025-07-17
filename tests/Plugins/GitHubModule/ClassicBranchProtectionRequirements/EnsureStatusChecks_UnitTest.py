# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for EnsureStatusChecks.py"""

import pytest

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.EnsureStatusChecks import (
    EnsureStatusChecks,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "branch": "main",
        "branch_protection_data": {
            "required_status_checks": {
                "checks": ["check1", "check2"],
            },
        },
    }


@pytest.fixture
def requirement():
    return EnsureStatusChecks()


class TestEnsureStatusChecks:
    def test_disabled(self, requirement, query_data):
        """Test disabled requirement"""
        requirement_args = {"disabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "The status check requirement has been explicitly disabled." in result.context

    def test_required_status_checks_missing(self, requirement, query_data):
        """Test when `required_status_checks` is missing"""
        query_data["branch_protection_data"] = {}
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_required_status_checks_none(self, requirement, query_data):
        """Test when `required_status_checks` is None"""
        query_data["branch_protection_data"] = {"required_status_checks": None}
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_checks_missing(self, requirement, query_data):
        """Test when `checks` is missing"""
        query_data["branch_protection_data"]["required_status_checks"] = {}
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "No status checks are configured." in result.context

    def test_checks_none(self, requirement, query_data):
        """Test when `checks` is None"""
        query_data["branch_protection_data"]["required_status_checks"] = {"checks": None}
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "No status checks are configured." in result.context

    def test_Successful(self, requirement, query_data):
        """Test successful"""
        query_data["branch_protection_data"]["required_status_checks"]["checks"] = ["check1", "check2"]
        requirement_args = {"disabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_SuccessfulGetDynamicArgDefinitions(self, requirement, query_data):
        """Test with GetDynamicArgDefinitions"""
        query_data["branch_protection_data"]["required_status_checks"]["checks"] = ["check1", "check2"]
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
