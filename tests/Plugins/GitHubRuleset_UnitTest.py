# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for the GitHub Rulesets Plugin"""

from typing import Any

from RepoAuditor.Requirement import EvaluateResult
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequireStatusChecks import RequireStatusChecks
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequireSignedCommits import (
    RequireSignedCommits,
)


def create_rule(name: str, rule_type: str, ruleset_name: str, parameters: dict[str, Any]):
    """Helper function to create rule structure"""
    return {
        "name": name,
        "type": rule_type,
        "ruleset": {"name": ruleset_name},
        "parameters": parameters,
    }


# ----------------------------------------------------------------------
class TestRequirePullRequests:
    """Unit tests for the RequirePullRequests requirement."""

    def test_Enabled(self):
        """Test if the rule is enabled on the main branch."""
        requirement = RequirePullRequests()
        context = {
            "rules": [
                create_rule(
                    name="PR Rules",
                    rule_type="pull_request",
                    ruleset_name="Ruleset Main",
                    parameters={},
                )
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Success
        assert "enforces Pull Requests" in result.context

    def test_Disabled(self):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequirePullRequests()
        context = {
            "rules": [
                create_rule(
                    name="Inactive PR Rules",
                    # Wrong rule type
                    rule_type="",
                    ruleset_name="Ruleset Main",
                    parameters={},
                )
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error

    def test_WrongTarget(self):
        """Test if rules are applied on the wrong branch."""
        requirement = RequirePullRequests()
        context = {
            "rules": [
                # GitHub behavior is to always give enforced rules on the specified target target.
                # Hence the rules here will be empty.
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self):
        """Test if no rules are applied on the main branch."""
        requirement = RequirePullRequests()
        context = {"rules": []}
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring Pull Requests found" in result.context


# ----------------------------------------------------------------------
class TestRequireSignedCommits:
    """Unit tests for the RequireSignedCommits requirement."""

    def test_Enabled(self):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireSignedCommits()
        context = {
            "rules": [
                create_rule(
                    name="Signing Rules",
                    rule_type="required_signatures",
                    ruleset_name="Ruleset Main",
                    parameters={},
                )
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Success
        assert "enforces Signed Commits" in result.context

    def test_Disabled(self):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireSignedCommits()
        context = {
            "rules": [
                create_rule(
                    name="Signing Rules",
                    # Wrong rule type
                    rule_type="pull_request",
                    ruleset_name="Ruleset Main",
                    parameters={},
                )
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error

    def test_PartialConfig(self):
        """Test for rules that are not actively enforced."""
        requirement = RequireSignedCommits()
        context = {
            "rules": [
                # GitHub only returns rules that are actively enforced
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self):
        """Test if no rules are applied on the main branch."""
        requirement = RequireSignedCommits()
        context = {"rules": []}
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring Signed Commits found" in result.context


# ----------------------------------------------------------------------
class TestRequireStatusChecks:
    """Unit tests for the RequireStatusChecks requirement."""

    def test_Enabled(self):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireStatusChecks()
        context = {
            "rules": [
                create_rule(
                    name="CI Checks",
                    rule_type="required_status_checks",
                    ruleset_name="Ruleset Main",
                    parameters={},
                )
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Success
        assert "enforces Status Checks" in result.context

    def test_EmptyChecks(self):
        """Test for Status Check rules which don't have an associated CI check."""
        requirement = RequireStatusChecks()
        context = {
            "rules": [
                # GitHub won't allow active status check rules
                # which don't have associated CI checks.
                # Hence empty.
            ]
        }
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self):
        """Test if no rules are applied on the main branch."""
        requirement = RequireStatusChecks()
        context = {"rules": []}
        result = requirement.Evaluate(context, {"true": True})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring Status Checks found" in result.context
