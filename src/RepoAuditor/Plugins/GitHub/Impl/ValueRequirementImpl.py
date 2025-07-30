# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ValueRequirementImpl object."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.Common import CreateIncompleteDataResult
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DoesNotApplyResult:
    """Evaluate result returned when a requirement does not apply."""

    reason: str


# ----------------------------------------------------------------------
class ValueRequirementImpl(Requirement):
    """Object that implements checking of metadata/settings are set to the specified value."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        default_value: str,
        github_value: Optional[str],
        get_configuration_value_func: Callable[[dict[str, Any]], str | DoesNotApplyResult | None],
        resolution: str,
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        missing_value_is_warning: bool = True,
    ) -> None:
        github_value = f"'{github_value}'" if github_value else "the entity"

        if subject is None:
            subject = github_value

        super().__init__(
            name,
            f"Validates that {subject} is set to '{{__expected_value}}'.",
            ExecutionStyle.Parallel,
            resolution,
            rationale,
            requires_explicit_include=requires_explicit_include,
        )

        self.github_value = github_value
        self.default_value = default_value
        self.get_configuration_value_func = get_configuration_value_func
        self.missing_value_is_warning = missing_value_is_warning

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            "value": (
                str,
                typer.Option(
                    self.default_value,
                    help=f"Ensures that {self.github_value} is set to the provided value.",
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
        expected_value = requirement_args.get("value", self.default_value)
        query_data["__expected_value"] = f"{expected_value}"

        result = self.get_configuration_value_func(query_data)
        if result is None:
            if self.missing_value_is_warning:
                return CreateIncompleteDataResult()

            return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, None)

        is_default_expected_value = expected_value == self.default_value

        if isinstance(result, DoesNotApplyResult):
            if is_default_expected_value:
                return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, result.reason)

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self.github_value} cannot be set to '{expected_value}' because {result.reason}",
            )

        result = str(result)

        if result != expected_value:
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self.github_value} must be set to '{expected_value}' (it is currently set to '{result}').",
                provide_resolution=True,
                provide_rationale=is_default_expected_value,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
