# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the EnableRequirementImpl object"""

import textwrap

from typing import Any, Callable, Optional

import typer

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement

from .Common import CreateIncompleteDataResult


# ----------------------------------------------------------------------
class EnableRequirementImpl(Requirement):
    """Object that implements settings that can be enabled/disabled."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        default_value: bool,
        dynamic_arg_name: str,
        github_settings_url_suffix: str,
        github_settings_section: str,
        github_settings_value: str,
        get_configuration_value_func: Callable[[dict[str, Any]], Optional[bool]],
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        unset_set_terminology: tuple[str, str] = ("unchecked", "checked"),
    ) -> None:
        github_settings_value = f"'{github_settings_value}'"

        if subject is None:
            subject = github_settings_value

        super(EnableRequirementImpl, self).__init__(
            name,
            f"Validates that {subject} is set to the expected value.",
            ExecutionStyle.Parallel,
            textwrap.dedent(
                f"""\
                1) Visit '{{session.github_url}}/{github_settings_url_suffix}'
                2) Locate the '{github_settings_section}' section
                3) Ensure that {github_settings_value} is {{__checked_desc}}
                """,
            ),
            rationale,
            requires_explicit_include=requires_explicit_include,
        )

        self._github_settings_value = github_settings_value
        self._default_value = default_value
        self._dynamic_arg_name = dynamic_arg_name
        self._get_configuration_value_func = get_configuration_value_func
        self._unset_set_terminology = unset_set_terminology

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            self._dynamic_arg_name: (
                bool,
                typer.Option(
                    False,
                    help=f"Ensures that the value for {self._github_settings_value} is set to {not self._default_value}.",
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

        expected_value = self._default_value

        if requirement_args[self._dynamic_arg_name]:
            expected_value = not expected_value
            provide_rationale = False
        else:
            provide_rationale = True

        if result != expected_value:
            query_data["__checked_desc"] = self._unset_set_terminology[int(expected_value)]

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self._github_settings_value} must be set to '{expected_value}' (it is currently set to '{result}').",
                provide_resolution=True,
                provide_rationale=provide_rationale,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
