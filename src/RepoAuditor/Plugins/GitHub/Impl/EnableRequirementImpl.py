# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the EnableRequirementImpl object."""

from collections.abc import Callable
from typing import Any, Optional

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.Common import CreateIncompleteDataResult
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class EnableRequirementImpl(Requirement):
    """Object that implements settings that can be enabled/disabled."""

    # ----------------------------------------------------------------------
    def __init__(  # noqa: PLR0913
        self,
        name: str,
        enabled_by_default: bool,  # noqa: FBT001
        dynamic_arg_name: str,
        github_settings_value: str,
        get_configuration_value_func: Callable[[dict[str, Any]], Optional[bool]],
        resolution: str,
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        unset_set_terminology: tuple[str, str] = ("unchecked", "checked"),
        missing_value_is_warning: bool = True,
    ) -> None:
        github_settings_value = f"'{github_settings_value}'"

        if subject is None:
            subject = github_settings_value

        super().__init__(
            name,
            f"Validates that {subject} is set to {{__expected_value}}.",
            ExecutionStyle.Parallel,
            resolution,
            rationale,
            requires_explicit_include=requires_explicit_include,
        )

        self.dynamic_arg_name = dynamic_arg_name
        self.github_settings_value = github_settings_value
        self.enabled_by_default = enabled_by_default
        self.get_configuration_value_func = get_configuration_value_func
        self.unset_set_terminology = unset_set_terminology
        self.missing_value_is_warning = missing_value_is_warning

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            self.dynamic_arg_name: (
                bool,
                typer.Option(
                    False,
                    help=f"Ensures that the check for {self.github_settings_value} is {'disabled' if self.enabled_by_default else 'enabled'}.",
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
        expected_value = self.enabled_by_default

        # The value of the dynamic arg doesn't matter as much as whether it was provided
        if requirement_args.get(self.dynamic_arg_name, False):
            expected_value = not expected_value
            provide_rationale = False
        else:
            provide_rationale = True

        query_data["__expected_value"] = expected_value

        result = self.get_configuration_value_func(query_data)
        if result is None:
            if query_data["session"].is_enterprise:
                return Requirement.EvaluateImplResult(
                    EvaluateResult.DoesNotApply,
                    (
                        "Please verify with your enterprise administrator "
                        f"that {self.github_settings_value} is enabled."
                    ),
                )

            if self.missing_value_is_warning:
                return CreateIncompleteDataResult()

            return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, None)

        if result != expected_value:
            query_data["__checked_desc"] = self.unset_set_terminology[int(expected_value)]

            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self.github_settings_value} must be set to '{expected_value}' (it is currently set to '{result}').",
                provide_resolution=True,
                provide_rationale=provide_rationale,
            )

        return Requirement.EvaluateImplResult(EvaluateResult.Success, None)
