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
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireSignedCommits import RequireSignedCommits
from RepoAuditor.Plugins.GitHub.RulesetRequirements.RequireStatusChecks import RequireStatusChecks
from RepoAuditor.Query import Query


class RulesetQuery(Query):
    """Query to validate GitHub repository rulesets."""

    def __init__(self) -> None:
        super().__init__(
            "RulesetQuery",
            ExecutionStyle.Parallel,
            [
                RequireStatusChecks(),
                RequirePullRequests(),
                RequireSignedCommits(),
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
            ruleset_respone = module_data["session"].get(f"rulesets/{rule['ruleset_id']}")
            ruleset_respone.raise_for_status()
            ruleset = ruleset_respone.json()
            rule["ruleset"] = ruleset

        return module_data
