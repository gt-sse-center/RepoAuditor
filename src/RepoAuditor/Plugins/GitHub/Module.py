# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubModule object."""

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule

from .ClassicBranchProtectionQuery import ClassicBranchProtectionQuery
from .DefaultBranchQuery import DefaultBranchQuery
from .StandardQuery import StandardQuery


# ----------------------------------------------------------------------
class GitHubModule(GitHubBaseModule):
    """Module for validating GitHub repository configuration settings."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "GitHub",
            "Validates GitHub configuration settings.",
            ExecutionStyle.Parallel,
            [
                StandardQuery(),
                DefaultBranchQuery(),
                ClassicBranchProtectionQuery(),
            ],
            requires_explicit_include=True,
        )
