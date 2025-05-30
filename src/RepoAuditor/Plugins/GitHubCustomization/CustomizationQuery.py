# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CustomizationQuery object."""

from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Query import ExecutionStyle, Query
from RepoAuditor.Plugins.GitHubCustomization.Requirements.CodeOwners import CodeOwners
from RepoAuditor.Plugins.GitHubCustomization.Requirements.Contributing import Contributing
from RepoAuditor.Plugins.GitHubCustomization.Requirements.IssueTemplates import IssueTemplates
from RepoAuditor.Plugins.GitHubCustomization.Requirements.PullRequestTemplates import PullRequestTemplate
from RepoAuditor.Plugins.GitHubCustomization.Requirements.SecurityPolicy import SecurityPolicy


class CustomizationQuery(Query):
    """Query with requirements that check for GitHub customization files."""

    def __init__(self) -> None:
        super().__init__(
            "CustomizationQuery",
            ExecutionStyle.Parallel,
            [
                CodeOwners(),
                Contributing(),
                IssueTemplates(),
                PullRequestTemplate(),
                SecurityPolicy(),
            ],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Get the data from an API session."""
        response = module_data["session"].get("")

        response.raise_for_status()
        response = response.json()

        module_data["standard"] = response

        return module_data
