# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Protected object."""

import textwrap
from typing import Any

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.Common import CreateIncompleteDataResult
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class Protected(Requirement):
    """Requirement to ensure that the mainline branch is protected."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        # Note that protected is set for the branch when creating a branch ruleset or a classic
        # branch protection rule.
        super().__init__(
            "Protected",
            "Ensures that the mainline branch is protected.",
            ExecutionStyle.Parallel,
            textwrap.dedent(
                """\
                1) Visit '{session.github_url}/settings/branches'
                2) Locate the 'Branch protection rules' section
                3) Protect the branch with a ruleset or classic branch protection rule
                """,
            ),
            textwrap.dedent(
                """\
                The default behavior is to protect the mainline branch.

                Reasons for this Default
                ------------------------
                - The mainline branch is the most important branch in a repository and should be protected.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            "disabled": (
                bool,
                typer.Option(
                    default=False,
                    help="Allow an unprotected mainline branch.",
                ),
            ),
        }

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        is_protected = query_data["default_branch_data"].get("protected", None)
        if is_protected is None:
            return CreateIncompleteDataResult()

        if requirement_args["disabled"]:
            expected_value = False
            provide_rationale = False
        else:
            expected_value = True
            provide_rationale = True

        if is_protected != expected_value:
            if expected_value:
                modifier = ""
                current_modifier = " not"
            else:
                modifier = " not"
                current_modifier = ""

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"The mainline branch must{modifier} be protected (it is currently{current_modifier} protected).",
                provide_resolution=True,
                provide_rationale=provide_rationale,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
