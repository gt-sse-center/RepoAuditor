# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for AllowMainlineForcePushesRule.py"""

from RepoAuditor.Plugins.GitHub.RulesetRequirements.AllowMainlineForcePushes import (
    AllowMainlineForcePushesRule,
)
from RepoAuditor.Requirement import EvaluateResult

from . import create_rule


class TestAllowMainlineForcePushesRule:
    """Unit tests for the AllowMainlineForcePushesRule requirement."""

    def test_Enabled(self, query_data):
        """Test if the rule is enabled on the main branch."""
        requirement = AllowMainlineForcePushesRule()

        query_data["rules"].append(
            create_rule(
                name="main",
                rule_type="non_fast_forward",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"yes": True})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, query_data):
        """Test if the rule is disabled by not providing the appropriate rule within the ruleset."""
        requirement = AllowMainlineForcePushesRule()

        query_data["rules"].append(
            create_rule(
                name="Random Rule",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(query_data, {"yes": True})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context
