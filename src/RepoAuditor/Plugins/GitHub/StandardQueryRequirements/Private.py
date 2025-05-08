# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Private object"""

import textwrap
from typing import Any

import typer

from dbrownell_Common.Types import override  # type: ignore[import-untyped]
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement

from ..Impl.Common import CreateIncompleteDataResult


# ----------------------------------------------------------------------
class Private(Requirement):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(Private, self).__init__(
            "Private",
            "Validates that the repository is set to the expected visibility.",
            ExecutionStyle.Parallel,
            textwrap.dedent(
                """\
                1) Visit '{session.github_url}/settings'
                2) Locate the 'Danger Zone' section
                3) Click the 'Change visibility button'
                4) Select 'Change to {__expected_visibility}'
                """,
            ),
            textwrap.dedent(
                """\
                The default behavior is to ensure that the repository is public.

                Reasons for this Default
                ------------------------
                - The vast majority of repositories hosted by GitHub are public.

                Reasons to Override this Default
                --------------------------------
                - Your repository really should be private.
                """,
            ),
        )

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            "true": (
                bool,
                typer.Option(
                    False,
                    help="Ensures that the repository's visibility is set to private.",
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
        result = query_data["standard"].get("private", None)

        if result is None:
            return CreateIncompleteDataResult()

        expect_private = requirement_args["true"]

        if result != expect_private:
            query_data["__expected_visibility"] = "private" if expect_private else "public"

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"The repository's visibility must be {query_data['__expected_visibility']}.",
                provide_resolution=True,
                provide_rationale=not expect_private,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
