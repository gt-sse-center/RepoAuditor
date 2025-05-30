# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ExistsRequirementImpl object."""

from typing import Any
from collections.abc import Sequence

import typer

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class ExistsRequirementImpl(Requirement):
    """Object that implements check if a file exists."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        dynamic_arg_name: str,
        github_file: str,
        possible_locations: Sequence[str],
        resolution: str,
        rationale: str,
        *,
        requires_explicit_include: bool = False,
    ) -> None:
        super().__init__(
            name,
            f"Validates that {github_file} file exists.",
            ExecutionStyle.Parallel,
            resolution,
            rationale,
            requires_explicit_include=requires_explicit_include,
        )

        self.dynamic_arg_name = dynamic_arg_name
        self.github_file = github_file
        self.possible_locations = possible_locations

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            self.dynamic_arg_name: (
                bool,
                typer.Option(
                    False,
                    help=f"Ensures that the customization file {self.github_file} exists.",
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
        if requirement_args[self.dynamic_arg_name]:
            for location in self.possible_locations:
                # Query for file location
                response = query_data["session"].get(f"contents/{location}")
                # If file is found, response will have status code 200
                if response.status_code == 200:
                    return Requirement.EvaluateImplResult(EvaluateResult.Success, None)

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"No {self.github_file} file found.",
                provide_resolution=True,
                provide_rationale=True,
            )

        # Requirement flag not set so DoesNotApply
        return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, None)
