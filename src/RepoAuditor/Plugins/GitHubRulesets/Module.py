# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubRulesetModule object."""

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule
from RepoAuditor.Plugins.GitHubRulesets.RulesetQuery import RulesetQuery


class GitHubRulesetsModule(GitHubBaseModule):
    """Module that validates GitHub repository rulesets."""

    def __init__(self) -> None:
        super().__init__(
            "GitHubRulesets",
            "Validates GitHub repository rulesets.",
            ExecutionStyle.Parallel,
            [
                RulesetQuery(),
            ],
            requires_explicit_include=True,
        )
