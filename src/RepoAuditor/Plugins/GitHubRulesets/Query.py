from typing import Any, Dict, Optional
from pathlib import Path

from dbrownell_Common.Types import override
from RepoAuditor.Impl.ParallelSequentialProcessor import ExecutionStyle
from RepoAuditor.Query import Query
from .Requirments.RequirePullRequests import RequirePullRequests
from .Requirments.RequireSignedCommits import RequireSignedCommits
from .Requirments.RequireStatusChecks import RequireStatusChecks
class RulesetQuery(Query):
    """Query to validate GitHub repository rulesets."""

    def __init__(self) -> None:
        super(RulesetQuery, self).__init__(
            "RulesetQuery",
            ExecutionStyle.Parallel,
            [
                RequireStatusChecks(),
                RequirePullRequests(),
                RequireSignedCommits()
            ]
        )

    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """
        Retrieves data required for validating GitHub rulesets.

        Args:
            module_data (dict): Dictionary containing initial data from the module.

        Returns:
            Optional[dict]: A dictionary containing ruleset-related data, or None if an error occurs.
        """
        try:
            # Get the session object from module_data
            session = module_data.get("session")
            if not session:
                print("RulesetQuery: Error - No GitHub session provided.")
                return None

            # Fetch ruleset data from the GitHub API
            print("RulesetQuery: Fetching ruleset data...")
            ruleset_data = session.request("GET", "/rulesets")

            # Add ruleset data to module_data
            module_data["ruleset_data"] = ruleset_data
            return module_data

        except Exception as e:
            print(f"RulesetQuery: Error in GetData: {str(e)}")
            import traceback

            traceback.print_exc()
            return None