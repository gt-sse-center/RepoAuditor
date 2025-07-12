# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CommunityStandardsModule object."""

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.CommunityStandards.CommunityStandardsQuery import CommunityStandardsQuery
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule


class CommunityStandardsModule(GitHubBaseModule):
    """Module that validates existence of repository files for Community Standards."""

    def __init__(self) -> None:
        super().__init__(
            "CommunityStandards",
            "Validates existence of repository files for Community Standards.",
            ExecutionStyle.Parallel,
            [
                CommunityStandardsQuery(),
            ],
            requires_explicit_include=True,
        )
