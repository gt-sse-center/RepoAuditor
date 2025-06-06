# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for the GitHub Rulesets Plugin"""

from RepoAuditor.Requirement import EvaluateResult
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequireStatusChecks import RequireStatusChecks
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequireSignedCommits import (
    RequireSignedCommits,
)


def create_ruleset(name, target, enforcement, parameters):
    """Helper function to create ruleset structure"""
    return {"name": name, "target": target, "enforcement": enforcement, "parameters": parameters}


# ----------------------------------------------------------------------
class TestRequirePullRequests:
    """Unit tests for the RequirePullRequests requirement."""

    def test_Enabled(self):
        requirement = RequirePullRequests()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="PR Rules",
                    target="branch",
                    enforcement="active",
                    parameters={"pull_request": {"required": True, "require_code_owner_review": True}},
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Success
        assert "enforces pull requests" in result.context

    def test_Disabled(self):
        requirement = RequirePullRequests()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Inactive PR Rules",
                    target="branch",
                    enforcement="disabled",  # Wrong enforcement
                    parameters={"pull_request": {"required": True}},
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_WrongTarget(self):
        requirement = RequirePullRequests()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Wrong Target Rules",
                    target="tag",  # Wrong target
                    enforcement="active",
                    parameters={"pull_request": {"required": True}},
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_MissingParameter(self):
        requirement = RequirePullRequests()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Partial Rules",
                    target="branch",
                    enforcement="active",
                    parameters={"other_rule": {}},  # Missing pull_request
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self):
        requirement = RequirePullRequests()  # type: ignore
        context = {"rulesets": []}
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring pull requests found" in result.context


# ----------------------------------------------------------------------
class TestRequireSignedCommits:
    """Unit tests for the RequireSignedCommits requirement."""

    def test_Enabled(self):
        requirement = RequireSignedCommits()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Signing Rules",
                    target="branch",
                    enforcement="active",
                    parameters={"commit_signatures": True},
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Success
        assert "enforces signed commits" in result.context

    def test_Disabled(self):
        requirement = RequireSignedCommits()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Inactive Signing",
                    target="branch",
                    enforcement="evaluate",  # Wrong enforcement
                    parameters={"commit_signatures": True},
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_PartialConfig(self):
        requirement = RequireSignedCommits()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Partial Config",
                    target="branch",
                    enforcement="active",
                    parameters={"commit_signatures": False},  # Explicitly disabled
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self):
        requirement = RequireSignedCommits()  # type: ignore
        context = {"rulesets": []}
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring signed commits found" in result.context


# ----------------------------------------------------------------------
class TestRequireStatusChecks:
    """Unit tests for the RequireStatusChecks requirement."""

    def test_Enabled(self):
        requirement = RequireStatusChecks()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="CI Checks",
                    target="branch",
                    enforcement="active",
                    parameters={
                        "required_status_checks": [
                            {"context": "ci-test"},
                            {"context": "security-scan"},
                        ]
                    },
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Success
        assert "enforces status checks" in result.context

    def test_EmptyChecks(self):
        requirement = RequireStatusChecks()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Empty Checks",
                    target="branch",
                    enforcement="active",
                    parameters={"required_status_checks": []},  # Empty list
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_InactiveRuleset(self):
        requirement = RequireStatusChecks()  # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Inactive Checks",
                    target="branch",
                    enforcement="disabled",  # Inactive
                    parameters={"required_status_checks": [{"context": "ci-test"}]},
                )
            ]
        }
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self):
        requirement = RequireStatusChecks()  # type: ignore
        context = {"rulesets": []}
        result = requirement.Evaluate(context, {})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring status checks found" in result.context
