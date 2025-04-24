# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CustomizationQuery object"""

from typing import Any, Optional
from pathlib import Path

from dbrownell_Common.Types import override

from RepoAuditor.Query import ExecutionStyle, Query

from .Requirements.IssueTemplates import IssueTemplates
from .Requirements.PullRequestTemplate import PullRequestTemplate
from .Requirements.SecurityPolicy import SecurityPolicy
from .Requirements.CodeOwners import CodeOwners
from .Requirements.Contributing import Contributing


class CustomizationQuery(Query):
    """Query with requirements that check for GitHub customization files."""

    def __init__(self) -> None:
        super(CustomizationQuery, self).__init__(
            "CustomizationQuery",
            ExecutionStyle.Parallel,
            [
                IssueTemplates(),
                PullRequestTemplate(),
                SecurityPolicy(),
                CodeOwners(),
                Contributing(),
            ],
        )

    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        try:

            # Get the repository path
            repo_path = module_data.get("repo_path")
            if not repo_path:
                print("CustomizationQuery: Error - No repository path provided")
                return None

            # Ensure repo_path is a Path object
            if isinstance(repo_path, str):
                repo_path = Path(repo_path)

            print(f"CustomizationQuery: Using repository path: {repo_path}")

            # Check if the path exists
            if not repo_path.exists():
                print(f"CustomizationQuery: Error - Repository path does not exist: {repo_path}")
                return None

            module_data["repo_path"] = repo_path
            return module_data

        except Exception as e:
            print(f"CustomizationQuery: Error in GetData: {str(e)}")
            import traceback

            traceback.print_exc()
            return None
