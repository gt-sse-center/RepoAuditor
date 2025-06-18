# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubCommunityStandardsModule object."""

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule
from RepoAuditor.Plugins.GitHubCommunityStandards.CommunityStandardsQuery import CommunityStandardsQuery


class GitHubCommunityStandardsModule(GitHubBaseModule):
    """Module that validates GitHub repository files for Community Standards."""

    def __init__(self) -> None:
        super().__init__(
            "GitHubCommunityStandards",
            "Validates GitHub repository files for Community Standards.",
            ExecutionStyle.Parallel,
            [
                CommunityStandardsQuery(),
            ],
            requires_explicit_include=True,
        )
