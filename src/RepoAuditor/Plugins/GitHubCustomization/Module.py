# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubCustomizationModule object."""

from typing import Any, Optional
from RepoAuditor.Module import ExecutionStyle, Module
from dbrownell_Common.TyperEx import TypeDefinitionItemType
from dbrownell_Common.Types import override


class GitHubCustomizationModule(Module):
    """Module that validates GitHub repository customization files."""

    def __init__(self) -> None:
        super().__init__(
            "GitHubCustomization",
            "Validates GitHub repository customization files.",
            ExecutionStyle.Parallel,
            [],  # Empty query list for now
            requires_explicit_include=False,
        )

    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Return the dynamic arguments for this module."""
        # Return an empty dictionary as we don't have any dynamic args yet
        return {}

    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:  # noqa: ARG002
        """Generate initial data for queries to use."""
        # Return an empty dictionary as we don't have any initial data yet
        return {}

    @override
    def Cleanup(self, dynamic_args: dict[str, Any]) -> None:
        """Clean up any resources created during execution."""
        # No resources to clean up in the minimal implementation
