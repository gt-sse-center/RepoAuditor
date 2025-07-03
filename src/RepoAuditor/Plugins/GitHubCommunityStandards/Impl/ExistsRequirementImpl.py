# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ExistsRequirementImpl object."""

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class ExistsRequirementImpl(Requirement):
    """Requirement which implements check if a file exists."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        github_file: str,
        possible_locations: Sequence[str],
        resolution: str,
        rationale: str,
        *,
        dynamic_arg_name: str = "unrequired",
        requires_explicit_include: bool = False,
    ) -> None:
        """Construct.

        Args:
            name (str): The name of the requirement. Used for unique identification.
            github_file (str): The name of the file in the GitHub repository being checked for.
            possible_locations (Sequence[str]): List of potential paths in the repo to check if `github_file` exists.
            resolution (str): Message on how to resolve the requirement in case of an error.
            rationale (str): Rationale message on why this requirement is needed.
            dynamic_arg_name (str, optional): Name of the runtime argument (e.g. from command line) to this requirement.Defaults to "unrequired", which if enabled causes the requirement to be skipped.
            requires_explicit_include (bool, optional): Flag checking if this requirement needs to be explicitly included in the invocation. Defaults to False.

        """
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
                    help=f"Disable requirement that the file {self.github_file} exists.",
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
        # Check if `dynamic_arg_name` is `not unrequired`.
        if not requirement_args[self.dynamic_arg_name]:
            for location in self.possible_locations:
                # Get full file path in temporary repo directory and check if it exists
                # This checks both upper case and lower case variants
                full_file_path = Path(query_data["repo_dir"].name) / Path(location)

                if full_file_path.exists():
                    # If full_file_path is a directory, check if it isn't empty
                    if full_file_path.is_dir() and any(full_file_path.iterdir()):
                        return Requirement.EvaluateImplResult(
                            EvaluateResult.Success,
                            f"File found in {location} directory of the repository",
                        )

                    return Requirement.EvaluateImplResult(
                        EvaluateResult.Success,
                        f"{self.github_file} found in repository",
                    )

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"No {self.github_file} file found.",
                provide_resolution=True,
                provide_rationale=True,
            )

        # Requirement flag not set so DoesNotApply
        return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, None)
