# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubCustomizationModule object."""

from typing import Any
from dbrownell_Common.Types import override

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule
from RepoAuditor.Plugins.GitHubCustomization.CustomizationQuery import CustomizationQuery


class GitHubCustomizationModule(GitHubBaseModule):
    """Module that validates GitHub repository customization files."""

    def __init__(self) -> None:
        super().__init__(
            "GitHubCustomization",
            "Validates GitHub repository customization files.",
            ExecutionStyle.Parallel,
            [
                CustomizationQuery(),
            ],
            requires_explicit_include=True,
        )

    @override
    def Cleanup(self, dynamic_args: dict[str, Any]) -> None:
        """Clean up any resources created during execution."""
        # No resources to clean up in the minimal implementation
