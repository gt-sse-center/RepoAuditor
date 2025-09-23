# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for RequireStatusChecksToPassRule.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireStatusChecksToPass import (
    RequireStatusChecksToPassRule,
)
from RepoAuditor.Requirement import EvaluateResult
from tests.Plugins.GitHubModule.RulesetRequirements import create_rule


class TestRequireStatusChecksToPassRule:
    """Unit tests for the RequireStatusChecksToPassRule requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireStatusChecksToPassRule()

        query_data["rules"].append(
            create_rule(
                name="CI Checks",
                rule_type="required_status_checks",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_EmptyChecks(self, query_data):
        """Test for Status Check rules which don't have an associated CI check."""
        requirement = RequireStatusChecksToPassRule()

        query_data["rules"] = [
            # GitHub won't allow active status check rules
            # which don't have associated CI checks.
            # Hence empty.
        ]

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self, query_data):
        """Test if no rules are applied on the main branch."""
        requirement = RequireStatusChecksToPassRule()

        query_data["rules"] = []

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context
