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
from RepoAuditor.Query import Query
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequirePullRequests import RequirePullRequests
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequireSignedCommits import RequireSignedCommits
from RepoAuditor.Plugins.GitHubRulesets.Requirements.RequireStatusChecks import RequireStatusChecks


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
        # Fetch ruleset data from the GitHub API
        ruleset_data = module_data["session"].get("rulesets")

        # Add ruleset data to module_data
        module_data["ruleset_data"] = ruleset_data
        return module_data
