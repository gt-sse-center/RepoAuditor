# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for EnsureStatusChecksRule.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.EnsureStatusChecks import EnsureStatusChecksRule
from RepoAuditor.Requirement import EvaluateResult
from tests.Plugins.GitHubModule.RulesetRequirements import create_rule


class TestEnsureStatusChecksRule:
    """Unit tests for the EnsureStatusChecksRule requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = EnsureStatusChecksRule()

        query_data["rules"].append(
            create_rule(
                name="main",
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={
                    "required_status_checks": [
                        "CI+CD",
                        "Additional Check",
                    ]
                },
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_NoStatusChecks(self, query_data):
        """Test if the rule is enabled but no status checks are provided."""
        requirement = EnsureStatusChecksRule()

        query_data["rules"].append(
            create_rule(
                name="main",
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={"required_status_checks": []},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context

    def test_Disabled(self, query_data):
        """Test if the rule is disabled by not providing the appropriate rule within the ruleset."""
        requirement = EnsureStatusChecksRule()

        query_data["rules"].append(
            create_rule(
                name="Random Rule",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context
