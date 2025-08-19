# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for RequireSignedCommits.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireSignedCommits import (
    RequireSignedCommits,
)
from RepoAuditor.Requirement import EvaluateResult

from . import create_rule


class TestRequireSignedCommits:
    """Unit tests for the RequireSignedCommits requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireSignedCommits()

        query_data["rules"].append(
            create_rule(
                name="Signing Rules",
                rule_type="required_signatures",
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
        requirement = RequireSignedCommits()
        query_data["rules"].append(
            create_rule(
                name="Signing Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_PartialConfig(self, query_data):
        """Test for rules that are not actively enforced."""
        requirement = RequireSignedCommits()
        query_data["rules"] = [
            # GitHub only returns rules that are actively enforced
        ]

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self, query_data):
        """Test if no rules are applied on the main branch."""
        requirement = RequireSignedCommits()
        query_data["rules"] = []
        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context
