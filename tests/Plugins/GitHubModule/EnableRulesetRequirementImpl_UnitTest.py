# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for the EnableRulesetRequirementImpl requirement implementation."""

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl
from RepoAuditor.Requirement import EvaluateResult


class TestEnableRulesetRequirementImpl:
    """Unit tests for the EnableRulesetRequirementImpl class."""

    def test_Constructor(self):
        """Test the EnableRulesetRequirementImpl constructor."""
        requirement = EnableRulesetRequirementImpl(
            name="Test Name",
            enabled_by_default=False,
            dynamic_arg_name="enabled",
            github_ruleset_type="Test Ruleset",
            github_ruleset_value="test_ruleset",
            get_configuration_value_func=lambda _: True,
            resolution="Test Resolution",
            rationale="Test rationale",
        )

        assert requirement.name == "Test Name"
        assert requirement.enabled_by_default is False
        assert requirement.dynamic_arg_name == "enabled"
        assert requirement.github_ruleset_type == "Test Ruleset"

    def test_Evaluate_Disabled(self):
        """Test the _EvaluateImpl method when dynamic arg is set to `enabled: False`."""
        requirement = EnableRulesetRequirementImpl(
            name="Test Name",
            enabled_by_default=False,
            dynamic_arg_name="enabled",
            github_ruleset_type="Test Ruleset",
            github_ruleset_value="test_ruleset",
            get_configuration_value_func=lambda _: True,
            resolution="Test Resolution",
            rationale="Test rationale",
        )
        query_data = {}
        requirement_args = {"enabled": False}
        result = requirement.Evaluate(query_data, requirement_args)
        # No rule and should be disabled, hence result is success
        assert result.result == EvaluateResult.Success

    def test_Evaluate_Disabled_Alternative(self):
        """Test the _EvaluateImpl method when dynamic arg is
        set to `disabled: True` but rule is active.
        """
        requirement = EnableRulesetRequirementImpl(
            name="True By Default",
            enabled_by_default=True,
            dynamic_arg_name="disabled",
            github_ruleset_type="Test Ruleset",
            github_ruleset_value="test_ruleset",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "valid_rule",
            resolution="Test Resolution",
            rationale="Test rationale",
        )
        query_data = {
            "rules": [
                {
                    "type": "valid_rule",
                    "ruleset": {
                        "name": "Valid",
                        "id": "01",
                    },
                },
            ]
        }
        requirement_args = {"disabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        # No rule and should be disabled, hence result is success
        assert result.result == EvaluateResult.Error
        assert "It should be set to False" in result.context

    def test_Evaluate_InvalidRule(self):
        """Test the _EvaluateImpl method when dynamic arg is set to `enabled: True` and the rule found is invalid."""
        requirement = EnableRulesetRequirementImpl(
            name="Test Name",
            enabled_by_default=False,
            dynamic_arg_name="enabled",
            github_ruleset_type="Test Ruleset",
            github_ruleset_value="test_ruleset",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "valid rule",
            resolution="Test Resolution",
            rationale="Test rationale",
        )
        query_data = {
            "rules": [
                {
                    "type": "invalid_rule",
                    "ruleset": {
                        "name": "Invalid",
                        "id": "00",
                    },
                },
            ]
        }
        requirement_args = {"enabled": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error

    def test_Evaluate_ValidRule(self):
        """Test the _EvaluateImpl method when dynamic arg is set to `enabled: True` and a valid rule is found."""
        requirement = EnableRulesetRequirementImpl(
            name="Test Name",
            enabled_by_default=False,
            dynamic_arg_name="enabled",
            github_ruleset_type="Test Ruleset",
            github_ruleset_value="test_ruleset",
            get_configuration_value_func=lambda rule: rule.get("type", "") == "valid_rule",
            resolution="Test Resolution",
            rationale="Test rationale",
        )
        query_data = {
            "rules": [
                {
                    "type": "valid_rule",
                    "ruleset": {
                        "name": "Valid",
                        "id": "00",
                    },
                }
            ]
        }
        requirement_args = {"enabled": True}
        result = requirement.Evaluate(query_data, requirement_args)

        assert result.result == EvaluateResult.Success
