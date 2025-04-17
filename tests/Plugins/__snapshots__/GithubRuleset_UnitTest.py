import pytest

from RepoAuditor.Requirement import EvaluateResult
from RepoAuditor.Plugins.GitHubRulesets.Requirments.RequirePullRequests import RequirePullRequests 
from RepoAuditor.Plugins.GitHubRulesets.Requirments.RequireStatusChecks import RequireStatusChecks
from RepoAuditor.Plugins.GitHubRulesets.Requirments.RequireSignedCommits import RequireSignedCommits

def create_ruleset(name, target, enforcement, parameters):
    """Helper function to create ruleset structure"""
    return {
        "name": name,
        "target": target,
        "enforcement": enforcement,
        "parameters": parameters
    }

# ----------------------------------------------------------------------
class TestRequirePullRequests:
    def test_enabled(self):
        requirement = RequirePullRequests() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="PR Rules",
                    target="branch",
                    enforcement="active",
                    parameters={
                        "pull_request": {
                            "required": True,
                            "require_code_owner_review": True
                        }
                    }
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Success
        assert "enforces pull requests" in result.context

    def test_disabled(self):
        requirement = RequirePullRequests() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Inactive PR Rules",
                    target="branch",
                    enforcement="disabled",  # Wrong enforcement
                    parameters={"pull_request": {"required": True}}
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_wrong_target(self):
        requirement = RequirePullRequests() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Wrong Target Rules",
                    target="tag",  # Wrong target
                    enforcement="active",
                    parameters={"pull_request": {"required": True}}
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_missing_parameter(self):
        requirement = RequirePullRequests() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Partial Rules",
                    target="branch",
                    enforcement="active",
                    parameters={"other_rule": {}}  # Missing pull_request
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_no_rulesets(self):
        requirement = RequirePullRequests() # type: ignore
        context = {"rulesets": []}
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring pull requests found" in result.context

# ----------------------------------------------------------------------
class TestRequireSignedCommits:
    def test_enabled(self):
        requirement = RequireSignedCommits() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Signing Rules",
                    target="branch",
                    enforcement="active",
                    parameters={"commit_signatures": True}
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Success
        assert "enforces signed commits" in result.context

    def test_disabled(self):
        requirement = RequireSignedCommits() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Inactive Signing",
                    target="branch",
                    enforcement="evaluate",  # Wrong enforcement
                    parameters={"commit_signatures": True}
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_partial_config(self):
        requirement = RequireSignedCommits() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Partial Config",
                    target="branch",
                    enforcement="active",
                    parameters={"commit_signatures": False}  # Explicitly disabled
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_no_rulesets(self):
        requirement = RequireSignedCommits() # type: ignore
        context = {"rulesets": []}
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring signed commits found" in result.context

# ----------------------------------------------------------------------
class TestRequireStatusChecks:
    def test_enabled(self):
        requirement = RequireStatusChecks() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="CI Checks",
                    target="branch",
                    enforcement="active",
                    parameters={
                        "required_status_checks": [
                            {"context": "ci-test"},
                            {"context": "security-scan"}
                        ]
                    }
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Success
        assert "enforces status checks" in result.context

    def test_empty_checks(self):
        requirement = RequireStatusChecks() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Empty Checks",
                    target="branch",
                    enforcement="active",
                    parameters={"required_status_checks": []}  # Empty list
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_inactive_ruleset(self):
        requirement = RequireStatusChecks() # type: ignore
        context = {
            "rulesets": [
                create_ruleset(
                    name="Inactive Checks",
                    target="branch",
                    enforcement="disabled",  # Inactive
                    parameters={
                        "required_status_checks": [
                            {"context": "ci-test"}
                        ]
                    }
                )
            ]
        }
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error

    def test_no_rulesets(self):
        requirement = RequireStatusChecks() # type: ignore
        context = {"rulesets": []}
        result = requirement._EvaluateImpl(context, {})
        assert result.result == EvaluateResult.Error
        assert "No active branch ruleset requiring status checks found" in result.context