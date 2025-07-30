# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the Private object."""

import textwrap
from typing import Any

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.Common import CreateIncompleteDataResult
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class Private(Requirement):
    """Validates that the repository is set to the expected visibility."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "Private",
            "Validates that the repository's visibility is set to '{__expected_visibility}'.",
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
        """Get the definitions for the arguments to this requirement."""
        return {
            "enabled": (
                bool,
                typer.Option(
                    default=False,
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
        expect_private = requirement_args.get("enabled", False)
        query_data["__expected_visibility"] = "private" if expect_private else "public"

        result = query_data["standard"].get("private", None)

        if result is None:
            return CreateIncompleteDataResult()

        if result != expect_private:
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"The repository's visibility must be {query_data['__expected_visibility']}.",
                provide_resolution=True,
                provide_rationale=not expect_private,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
