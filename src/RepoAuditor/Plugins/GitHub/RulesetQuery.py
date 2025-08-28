# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RulesetQuery object."""

from typing import Any, Optional

from dbrownell_Common.Types import override

from RepoAuditor.Impl.ParallelSequentialProcessor import ExecutionStyle
from RepoAuditor.Plugins.GitHub.RulesetRequirements.BlockMainlineForcePushes import (
    BlockMainlineForcePushesRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.DismissStalePullRequestApprovals import (
    DismissStalePullRequestApprovalsRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.EnsureStatusChecks import EnsureStatusChecksRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireApprovalMostRecentPush import (
    RequireApprovalMostRecentPushRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireApprovals import RequireApprovalsRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireCodeOwnerReview import RequireCodeOwnerReviewRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireCodeScanningResults import (
    RequireCodeScanningResultsRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireConversationResolution import (
    RequireConversationResolutionRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireLinearHistory import RequireLinearHistoryRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireSignedCommits import RequireSignedCommits
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireStatusChecksToPass import (
    RequireStatusChecksToPassRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireSuccessfulDeployments import (
    RequireSuccessfulDeploymentsRule,
)
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireUpToDateBranches import RequireUpToDateBranchesRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RestrictCreations import RestrictCreationsRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RestrictDeletions import RestrictDeletionsRule
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RestrictUpdates import RestrictUpdatesRule
from RepoAuditor.Query import Query


class RulesetQuery(Query):
    """Query to validate GitHub repository rulesets."""

    def __init__(self) -> None:
        super().__init__(
            "RulesetQuery",
            ExecutionStyle.Parallel,
            [
                RestrictCreationsRule(),
                RestrictUpdatesRule(),
                RestrictDeletionsRule(),
                RequireLinearHistoryRule(),
                RequireSuccessfulDeploymentsRule(),
                RequireSignedCommits(),
                RequirePullRequests(),
                RequireApprovalsRule(),
                DismissStalePullRequestApprovalsRule(),
                RequireCodeOwnerReviewRule(),
                RequireApprovalMostRecentPushRule(),
                RequireConversationResolutionRule(),
                RequireStatusChecksToPassRule(),
                RequireUpToDateBranchesRule(),
                EnsureStatusChecksRule(),
                BlockMainlineForcePushesRule(),
                RequireCodeScanningResultsRule(),
            ],
        )

    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Retrieve data required for validating GitHub rulesets.

        Args:
            module_data (dict): Dictionary containing initial data from the module.

        Returns:
            Optional[dict]: A dictionary containing ruleset-related
            data, or None if an error occurs.

        """
        branch = module_data.get("branch")
        if branch is None:
            # Get the default branch name
            response = module_data["session"].get("")

            response.raise_for_status()
            response = response.json()

            branch = response["default_branch"]

        # Record the branch name
        module_data["branch"] = branch

        # Fetch ruleset data for a specific branch.
        # This only returns active rules on the branch
        rules_response = module_data["session"].get(f"rules/branches/{branch}")

        rules_response.raise_for_status()

        # Add ruleset data to module_data
        module_data["rules"] = rules_response.json()

        # Also get the associated ruleset for each rule
        for rule in module_data["rules"]:
            ruleset_response = module_data["session"].get(f"rulesets/{rule['ruleset_id']}")
            ruleset_response.raise_for_status()
            ruleset = ruleset_response.json()
            rule["ruleset"] = ruleset

        return module_data
