# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHub/Impl/ValueRequirementImpl.py"""

import pytest

from RepoAuditor.Plugins.GitHub.Impl.ValueRequirementImpl import DoesNotApplyResult, ValueRequirementImpl
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def requirement():
    return ValueRequirementImpl(
        "TestValueRequirement",
        "42",
        "Test Value Requirement",
        lambda data: data.get("result", None),
        "",
        "",
    )


@pytest.fixture
def requirement_does_not_apply_result():
    return ValueRequirementImpl(
        "TestValueRequirement",
        "42",
        None,
        lambda data: DoesNotApplyResult(""),
        "",
        "",
    )


class TestValueRequirementImpl:
    """Test the ValueRequirementImpl class."""

    def test_ResultIsNone(self, requirement):
        """Test pathway where result value is None."""
        query_data = {"result": None}
        requirement_args = {"value": 0}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data" in result.context

    def test_ResultDoesntMatchExpectedValue(self, requirement):
        """Test pathway where result value and expected value don't match."""
        query_data = {"result": "43"}
        requirement_args = {"value": "40"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "'Test Value Requirement' must be set to '40' (it is currently set to '43')." in result.context

    def test_Successful(self, requirement):
        """Test successful."""
        query_data = {"result": "42"}
        requirement_args = {"value": "42"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_SuccessfulGetDynamicArgDefinitions(self, requirement):
        """Test successful with GetDynamicArgDefinitions/"""
        query_data = {"result": "42"}
        requirement_args = {}
        for key, value in requirement.GetDynamicArgDefinitions().items():
            requirement_args[key] = value[1].default
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_MissingValueIsWarning(self):
        """Test for result when missing_value_is_warning is False."""
        requirement = ValueRequirementImpl(
            "TestValueRequirement",
            "42",
            "Test Value Requirement",
            lambda data: data.get("result", None),
            "",
            "",
            missing_value_is_warning=False,
        )

        query_data = {"result": None}
        requirement_args = {"value": 0}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert result.context is None

    def test_ExpectedValueIsDefault(self, requirement_does_not_apply_result):
        """Test pathway where expected value is default."""
        query_data = {"result": "43"}
        requirement_args = {"value": "42"}
        result = requirement_does_not_apply_result.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply

    def test_ResultDoesNotApply(self, requirement_does_not_apply_result):
        """Test pathway where result is DoesNotApplyResult."""
        query_data = {"result": "42"}
        requirement_args = {"value": "43"}
        result = requirement_does_not_apply_result.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "the entity cannot be set to '43' because " in result.context
