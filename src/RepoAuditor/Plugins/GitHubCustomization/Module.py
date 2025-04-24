# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubCustomizationModule object"""

from RepoAuditor.Module import ExecutionStyle, Module
from .Query import CustomizationQuery


class GitHubCustomizationModule(Module):
    """Module that validates GitHub repository customization files."""

    def __init__(self) -> None:
        super(GitHubCustomizationModule, self).__init__(
            "GitHubCustomization",
            "Validates GitHub repository customization files.",
            ExecutionStyle.Parallel,
            [],  # Empty query list for now
            requires_explicit_include=False,
        )
