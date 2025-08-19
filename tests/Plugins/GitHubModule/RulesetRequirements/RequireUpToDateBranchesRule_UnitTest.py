# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for AllowMainlineForcePushesRule.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireUpToDateBranches import (
    RequireUpToDateBranchesRule,
)
from RepoAuditor.Requirement import EvaluateResult

from . import create_rule


class TestRequireUpToDateBranchesRule:
    """Unit tests for the RequireUpToDateBranchesRule requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireUpToDateBranchesRule()

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={"strict_required_status_checks_policy": True},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = RequireUpToDateBranchesRule()

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={"strict_required_status_checks_policy": False},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireUpToDateBranchesRule()

        query_data["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
