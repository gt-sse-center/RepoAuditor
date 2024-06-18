# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the Description object"""

import textwrap

from typing import Any, Optional

import typer

from dbrownell_Common.Types import override  # type: ignore[import-untyped]
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement

from ..Impl.Common import CreateIncompleteDataResult


# ----------------------------------------------------------------------
class Description(Requirement):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(Description, self).__init__(
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
        return {
            "allow-empty": (
                bool,
                typer.Option(
                    False,
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

        if "description" not in standard_data:
            return CreateIncompleteDataResult()

        result = standard_data["description"]

        expect_description = not requirement_args["allow-empty"]

        if expect_description and not result:
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                "The repository's description must be not be empty.",
                provide_resolution=True,
                provide_rationale=expect_description,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
