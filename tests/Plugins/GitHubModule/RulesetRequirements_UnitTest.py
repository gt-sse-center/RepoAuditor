# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for the GitHub Rulesets Plugin"""

from typing import Any

import pytest

from RepoAuditor.Plugins.GitHub.RulesetRequirements.AllowMainlineForcePushes import (
    AllowMainlineForcePushesRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.DismissStalePullRequestApprovals import (
    DismissStalePullRequestApprovalsRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.EnsureStatusChecks import EnsureStatusChecksRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireApprovalMostRecentPush import (
    RequireApprovalMostRecentPushRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireApprovals import RequireApprovalsRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireCodeOwnerReview import (
    RequireCodeOwnerReviewRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireConversationResolution import (
    RequireConversationResolutionRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireSignedCommits import (
    RequireSignedCommits,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireStatusChecksToPass import (
    RequireStatusChecksToPassRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireUpToDateBranches import (
    RequireUpToDateBranchesRule,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture(name="context")
def context_fixture(session):
    context = {
        "session": session,
        "branch": "main",
        "rules": [],
    }
    return context


def create_rule(
    name: str, rule_type: str, ruleset_name: str, parameters: dict[str, Any], ruleset_id: str = "0"
):
    """Helper function to create rule structure"""
    return {
        "name": name,
        "type": rule_type,
        "ruleset_id": ruleset_id,
        "ruleset": {"name": ruleset_name},
        "parameters": parameters,
    }


# ----------------------------------------------------------------------
class TestRequirePullRequests:
    """Unit tests for the RequirePullRequests requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequirePullRequests()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequirePullRequests()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": True})
        assert result.result == EvaluateResult.Success

    def test_WrongTarget(self, context):
        """Test if rules are applied on the wrong branch."""
        requirement = RequirePullRequests()
        context["rules"] = [
            # GitHub behavior is to always give enforced rules on the specified target target.
            # Hence the rules here will be empty.
        ]

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self, context):
        """Test if no rules are applied on the main branch."""
        requirement = RequirePullRequests()
        context["rules"] = []
        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context


# ----------------------------------------------------------------------
class TestRequireApprovalsRule:
    """Unit tests for the RequireApprovalsRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireApprovalsRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"required_approving_review_count": 1},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = RequireApprovalsRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"required_approving_review_count": 0},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireApprovalsRule()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error


# ----------------------------------------------------------------------
class TestDismissStalePullRequestApprovalsRule:
    """Unit tests for the DismissStalePullRequestApprovalsRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = DismissStalePullRequestApprovalsRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"dismiss_stale_reviews_on_push": True},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = DismissStalePullRequestApprovalsRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"dismiss_stale_reviews_on_push": False},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = DismissStalePullRequestApprovalsRule()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error


# ----------------------------------------------------------------------
class TestRequireCodeOwnerReviewRule:
    """Unit tests for the RequireCodeOwnerReviewRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireCodeOwnerReviewRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"require_code_owner_review": True},
            )
        )

        result = requirement.Evaluate(context, {"yes": True})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = RequireCodeOwnerReviewRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"require_code_owner_review": False},
            )
        )

        result = requirement.Evaluate(context, {"yes": True})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireCodeOwnerReviewRule()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"yes": True})
        assert result.result == EvaluateResult.Error


# ----------------------------------------------------------------------
class TestRequireApprovalMostRecentPushRule:
    """Unit tests for the RequireApprovalMostRecentPushRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireApprovalMostRecentPushRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"require_last_push_approval": True},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = RequireApprovalMostRecentPushRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"require_last_push_approval": False},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireApprovalMostRecentPushRule()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error


# ----------------------------------------------------------------------
class TestRequireConversationResolutionRule:
    """Unit tests for the RequireConversationResolutionRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireConversationResolutionRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"required_review_thread_resolution": True},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = RequireConversationResolutionRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={"required_review_thread_resolution": False},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireConversationResolutionRule()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error


# ----------------------------------------------------------------------
class TestRequireSignedCommits:
    """Unit tests for the RequireSignedCommits requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireSignedCommits()

        context["rules"].append(
            create_rule(
                name="Signing Rules",
                rule_type="required_signatures",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireSignedCommits()
        context["rules"].append(
            create_rule(
                name="Signing Rules",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_PartialConfig(self, context):
        """Test for rules that are not actively enforced."""
        requirement = RequireSignedCommits()
        context["rules"] = [
            # GitHub only returns rules that are actively enforced
        ]

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self, context):
        """Test if no rules are applied on the main branch."""
        requirement = RequireSignedCommits()
        context["rules"] = []
        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context


# ----------------------------------------------------------------------
class TestRequireStatusChecksToPassRule:
    """Unit tests for the RequireStatusChecksToPassRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireStatusChecksToPassRule()

        context["rules"].append(
            create_rule(
                name="CI Checks",
                rule_type="required_status_checks",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_EmptyChecks(self, context):
        """Test for Status Check rules which don't have an associated CI check."""
        requirement = RequireStatusChecksToPassRule()

        context["rules"] = [
            # GitHub won't allow active status check rules
            # which don't have associated CI checks.
            # Hence empty.
        ]

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_NoRulesets(self, context):
        """Test if no rules are applied on the main branch."""
        requirement = RequireStatusChecksToPassRule()

        context["rules"] = []

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context


# ----------------------------------------------------------------------
class TestRequireUpToDateBranchesRule:
    """Unit tests for the RequireUpToDateBranchesRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = RequireUpToDateBranchesRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={"strict_required_status_checks_policy": True},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the value as false.
        """
        requirement = RequireUpToDateBranchesRule()

        context["rules"].append(
            create_rule(
                name="PR Rules",
                # Wrong rule type
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={"strict_required_status_checks_policy": False},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error

    def test_WrongRuleType(self, context):
        """Test if the required rule is disabled on the main branch
        by providing the wrong rule type.
        """
        requirement = RequireUpToDateBranchesRule()

        context["rules"].append(
            create_rule(
                name="Inactive PR Rules",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="Ruleset Main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error


# ----------------------------------------------------------------------
class TestEnsureStatusChecksRule:
    """Unit tests for the EnsureStatusChecksRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = EnsureStatusChecksRule()

        context["rules"].append(
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

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_NoStatusChecks(self, context):
        """Test if the rule is enabled but no status checks are provided."""
        requirement = EnsureStatusChecksRule()

        context["rules"].append(
            create_rule(
                name="main",
                rule_type="required_status_checks",
                ruleset_name="main",
                parameters={"required_status_checks": []},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context

    def test_Disabled(self, context):
        """Test if the rule is disabled by not providing the appropriate rule within the ruleset."""
        requirement = EnsureStatusChecksRule()

        context["rules"].append(
            create_rule(
                name="Random Rule",
                # Wrong rule type
                rule_type="pull_request",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"no": False})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context


# ----------------------------------------------------------------------
class TestAllowMainlineForcePushesRule:
    """Unit tests for the AllowMainlineForcePushesRule requirement."""

    def test_Enabled(self, context):
        """Test if the rule is enabled on the main branch."""
        requirement = AllowMainlineForcePushesRule()

        context["rules"].append(
            create_rule(
                name="main",
                rule_type="non_fast_forward",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"yes": True})
        assert result.result == EvaluateResult.Success
        assert f"{requirement.github_settings_value} is enabled" in result.context

    def test_Disabled(self, context):
        """Test if the rule is disabled by not providing the appropriate rule within the ruleset."""
        requirement = AllowMainlineForcePushesRule()

        context["rules"].append(
            create_rule(
                name="Random Rule",
                # Wrong rule type
                rule_type="push_request",
                ruleset_name="main",
                parameters={},
            )
        )

        result = requirement.Evaluate(context, {"yes": True})
        assert result.result == EvaluateResult.Error
        assert f"No active branch ruleset with {requirement.github_settings_value} found" in result.context
