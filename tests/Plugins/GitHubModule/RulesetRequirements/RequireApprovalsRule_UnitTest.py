# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for RequireApprovalsRule.py"""

import pytest

from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireApprovals import RequireApprovalsRule
from RepoAuditor.Requirement import EvaluateResult

from . import create_rule


@pytest.fixture(name="requirement")
def requirement_fixture():
    return RequireApprovalsRule()


class TestRequireApprovalsRule:
    """Unit tests for the RequireApprovalsRule requirement."""

    def test_Enabled(self, requirement, query_data):
        """Test if the rule is enabled on the main branch."""

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"required_approving_review_count": 1},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, requirement, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"required_approving_review_count": 0},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, requirement, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """

        query_data["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoneRuleType(self, requirement, query_data):
        """Test behavior when the rule type provided is None."""

        query_data["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # None rule type
                rule_type=None,
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
