# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the EnableRequirementImpl object."""

from collections.abc import Callable
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRequirementImpl import EnableRequirementImpl
from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
class EnableRulesetRequirementImpl(EnableRequirementImpl):
    """Object that implements ruleset settings that can be enabled/disabled."""

    # ----------------------------------------------------------------------
    def __init__(  # noqa: PLR0913
        self,
        name: str,
        default_value: bool,  # noqa: FBT001
        dynamic_arg_name: str,
        github_ruleset_type: str,
        github_ruleset_value: str,
        get_configuration_value_func: Callable[[dict[str, Any]], Optional[bool]],
        resolution: str,
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        unset_set_terminology: tuple[str, str] = ("unchecked", "checked"),
        missing_value_is_warning: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            default_value=default_value,
            dynamic_arg_name=dynamic_arg_name,
            github_settings_value=github_ruleset_value,
            get_configuration_value_func=get_configuration_value_func,
            resolution=resolution,
            rationale=rationale,
            subject=subject,
            requires_explicit_include=requires_explicit_include,
            unset_set_terminology=unset_set_terminology,
            missing_value_is_warning=missing_value_is_warning,
        )

        self.github_ruleset_type = github_ruleset_type

    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        if requirement_args[self.dynamic_arg_name]:
            # Get the rules for the specified branch
            rules = query_data.get("rules", [])

            for rule in rules:
                if self.get_configuration_value_func(rule):
                    # Get the ruleset associated with the rule
                    ruleset = rule["ruleset"]
                    return self.EvaluateImplResult(
                        EvaluateResult.Success,
                        f"Ruleset '{ruleset['name']}' enforces {self.github_ruleset_type}",
                    )

            return self.EvaluateImplResult(
                EvaluateResult.Error,
                f"No active branch ruleset requiring {self.github_ruleset_type} found",
                provide_resolution=True,
                provide_rationale=True,
            )

        # Requirement flag not set so DoesNotApply
        return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply, None)
