# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Description object."""

import textwrap
from typing import Any

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.Common import CreateIncompleteDataResult
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class Description(Requirement):
    """Requirement to validate a repository's description."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "Description",
            "Validates a repository's description.",
            ExecutionStyle.Parallel,
            textwrap.dedent(
                """\
                1) Visit '{session.github_url}'
                2) Locate the 'About' section
                3) Click the gear icon
                4) Add a description
                """,
            ),
            textwrap.dedent(
                """\
                The default behavior is to require a repository description.

                Reasons for this Default
                ------------------------
                - A short description is helpful with browsing for repositories associated with a user or organization.

                Reasons to Override this Default
                --------------------------------
                - You do not want to spend time writing a short description.
                """,
            ),
        )

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            "allow-empty": (
                bool,
                typer.Option(
                    default=False,
                    help="Allow an empty repository description.",
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
        standard_data = query_data["standard"]

        result = standard_data.get("description", None)
        if result is None:
            return CreateIncompleteDataResult()

        expect_description = not requirement_args["allow-empty"]

        if expect_description and not result:
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                "The repository's description must be not be empty.",
                provide_resolution=True,
                provide_rationale=expect_description,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
