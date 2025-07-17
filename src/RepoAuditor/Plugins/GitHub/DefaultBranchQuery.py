# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the DefaultBranchQuery object."""

from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.DefaultBranchRequirements.Protected import Protected
from RepoAuditor.Query import ExecutionStyle, Query


# ----------------------------------------------------------------------
class DefaultBranchQuery(Query):
    """Query with requirements that operate on branch information."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "DefaultBranchQuery",
            ExecutionStyle.Parallel,
            [
                Protected(),
            ],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Get the data from an API session."""
        # Get the default branch name
        response = module_data["session"].get("")

        response.raise_for_status()
        response = response.json()

        module_data["default_branch"] = response["default_branch"]

        # Get the information for the default branch
        response = module_data["session"].get(f"branches/{module_data['default_branch']}")

        response.raise_for_status()
        response = response.json()

        module_data["default_branch_data"] = response

        return module_data
