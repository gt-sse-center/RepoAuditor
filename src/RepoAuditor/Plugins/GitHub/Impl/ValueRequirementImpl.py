# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ValueRequirementImpl object"""

import textwrap

from dataclasses import dataclass
from typing import Any, Callable, Optional

import typer

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement

from .Common import CreateIncompleteDataResult


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class DoesNotApplyResult:
    """Evaluate result returned when a requirement does not apply."""

    reason: str


# ----------------------------------------------------------------------
class ValueRequirementImpl(Requirement):
    """Object that implements settings specified by a value."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        default_value: str,
        github_settings_url_suffix: str,
        github_settings_section: Optional[str],
        github_settings_value: Optional[str],
        get_configuration_value_func: Callable[[dict[str, Any]], str | DoesNotApplyResult | None],
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
    ) -> None:
        if github_settings_value is None:
            github_settings_value = "the entity"
        else:
            github_settings_value = f"'{github_settings_value}'"

        if subject is None:
            subject = github_settings_value

        if github_settings_section is None:
            resolution = "No Resolution Instructions are available."
        else:
            resolution = textwrap.dedent(
                f"""\
                1) Visit '{{session.github_url}}/{github_settings_url_suffix}'
                2) Locate the '{github_settings_section}' section
                3) Ensure that {github_settings_value} is set to {{__expected_value}}
                """,
            )

        super(ValueRequirementImpl, self).__init__(
            name,
            f"Validates that {subject} is set to the expected value.",
            ExecutionStyle.Parallel,
            resolution,
            rationale,
            requires_explicit_include=requires_explicit_include,
        )

        self._github_settings_value = github_settings_value
        self._default_value = default_value
        self._get_configuration_value_func = get_configuration_value_func

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            "value": (
                str,
                typer.Option(
                    self._default_value,
                    help=f"Ensures that {self._github_settings_value} is set to the provided value.",
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
        result = self._get_configuration_value_func(query_data)

        if result is None:
            return CreateIncompleteDataResult()

        expected_value = requirement_args["value"]
        is_default_expected_value = expected_value == self._default_value

        if isinstance(result, DoesNotApplyResult):
            if is_default_expected_value:
                return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, result.reason)

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self._github_settings_value} cannot be set to '{expected_value}' because {result.reason}",
            )

        if result != expected_value:
            query_data["__expected_value"] = f"'{expected_value}'"

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self._github_settings_value} must be set to '{expected_value}' (it is currently set to '{result}').",
                provide_resolution=True,
                provide_rationale=is_default_expected_value,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
