# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubModule object."""

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionQuery import ClassicBranchProtectionQuery
from RepoAuditor.Plugins.GitHub.DefaultBranchQuery import DefaultBranchQuery
from RepoAuditor.Plugins.GitHub.RulesetQuery import RulesetQuery
from RepoAuditor.Plugins.GitHub.StandardQuery import StandardQuery
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule


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
                RulesetQuery(),
            ],
            requires_explicit_include=True,
        )
