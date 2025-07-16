# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the EnsureStatusChecks object."""

import textwrap
from typing import Any

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class EnsureStatusChecks(Requirement):
    """Ensure that status checks have been enabled for the branch."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "EnsureStatusChecks",
            "Ensure that status checks have been enabled for the '{branch}' branch.",
            ExecutionStyle.Parallel,
            textwrap.dedent(
                """\
                1) Visit '{session.github_url}/settings/branches'
                2) Locate the 'Branch protection rules' section
                3) Click the 'Edit' button next to the branch '{branch}'
                4) Locate the 'Protect matching branches' section
                5) Locate the 'Require status checks to pass before merging' section
                6) Add status checks that must pass before merging
                """,
            ),
            textwrap.dedent(
                """\
                The default behavior is to require the specification of at least one status check that must pass before merging.

                Reasons for this Default
                ------------------------
                - A Continuous Integration process must be gated by some activity, action, or work flow.

                Reasons to Override this Default
                --------------------------------
                - Code reviews are sufficient to ensure the quality of pull requests before they are merged into the branch
                  (this is not recommended).
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
                    help="If set, status checks will not be enforced.",
                ),
            ),
        }

    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        if requirement_args["disabled"]:
            return Requirement.EvaluateImplResult(
                EvaluateResult.DoesNotApply,
                "The status check requirement has been explicitly disabled.",
            )

        settings = query_data["branch_protection_data"].get("required_status_checks", None)
        if settings is None:
            return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, None)

        settings = settings.get("checks", None)
        if not settings:
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                "No status checks are configured.",
                provide_resolution=True,
                provide_rationale=True,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
