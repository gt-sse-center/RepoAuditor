# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for the RequirePullRequests.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Requirement import EvaluateResult

from . import create_rule


class TestRequirePullRequests:
    """Unit tests for the RequirePullRequests requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = RequirePullRequests()

        query_data["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, query_data):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequirePullRequests()

        query_data["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": True})
        assert result.result == EvaluateResult.Success

    def test_WrongTarget(self, query_data):
        """Test if rules are applied on the wrong branch."""
        requirement = RequirePullRequests()
        query_data["rules"] = [
            # GitHub behavior is to always give enforced rules on the specified target target.
            # Hence the rules here will be empty.
        ]

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self, query_data):
        """Test if no rules are applied on the main branch."""
        requirement = RequirePullRequests()
        query_data["rules"] = []
        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context
