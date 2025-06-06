# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubRulesetModule object."""

import typer

from dbrownell_Common.TyperEx import TypeDefinitionItemType
from dbrownell_Common.Types import override

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule
from RepoAuditor.Plugins.GitHubRulesets.RulesetQuery import RulesetQuery


class GitHubRulesetModule(GitHubBaseModule):
    """Module that validates GitHub repository rulesets."""

    def __init__(self) -> None:
        super().__init__(
            "GitHubRuleset",
            "Validates GitHub repository rulesets.",
            ExecutionStyle.Parallel,
            [RulesetQuery()],
            requires_explicit_include=True,
        )

    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            "url": (
                str,
                typer.Option(
                    ...,
                    help="[REQUIRED] GitHub repository URL (e.g., https://github.com/owner/repo).",
                ),
            ),
            "branch": (
                str,
                typer.Option(
                    None,
                    help="Branch to evaluate. The default branch will be used if not specified.",
                ),
            ),
        }
