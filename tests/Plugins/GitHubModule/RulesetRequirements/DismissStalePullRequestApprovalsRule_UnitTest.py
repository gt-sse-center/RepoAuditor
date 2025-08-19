# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for DismissStalePullRequestApprovalsRule.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.DismissStalePullRequestApprovals import (
    DismissStalePullRequestApprovalsRule,
)
from RepoAuditor.Requirement import EvaluateResult

from . import create_rule


class TestDismissStalePullRequestApprovalsRule:
    """Unit tests for the DismissStalePullRequestApprovalsRule requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = DismissStalePullRequestApprovalsRule()

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"dismiss_stale_reviews_on_push": True},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = DismissStalePullRequestApprovalsRule()

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"dismiss_stale_reviews_on_push": False},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = DismissStalePullRequestApprovalsRule()

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
