# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the EnableRequirementImpl object."""

import textwrap
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
        enabled_by_default: bool,  # noqa: FBT001
        dynamic_arg_name: str,
        github_ruleset_type: str,
        github_ruleset_value: str,
        get_configuration_value_func: Callable[[dict[str, Any]], Optional[bool]],
        rationale: str,
        resolution: Optional[str] = None,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        unset_set_terminology: tuple[str, str] = ("disabled", "enabled"),
        missing_value_is_warning: bool = True,
    ) -> None:
        if resolution is None:
            resolution = textwrap.dedent(
                """\
                1) Visit '{session.github_url}/settings/rules'.
                2) Find or create a ruleset on the branch '{branch}'.
                3) Go to '{__ruleset_value}'.
                4) {__enabled_str} the rule.
                """
            )

        super().__init__(
            name=name,
            enabled_by_default=enabled_by_default,
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
    def _GetValue(
        self,
        rule: dict[str, Any],
    ) -> Optional[bool]:
        rule_type = rule.get("type")
        if rule_type is None:
            return None

        return rule_type == self.github_ruleset_type

    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        expected_rule_enabled = self.enabled_by_default

        # The value of the dynamic arg doesn't matter as much as whether it was provided
        if requirement_args.get(self.dynamic_arg_name, False):
            expected_rule_enabled = not expected_rule_enabled
            provide_rationale = False
        else:
            provide_rationale = True

        query_data["__expected_value"] = expected_rule_enabled
        query_data["__enabled_str"] = "Enable" if expected_rule_enabled else "Disable"
        # ruleset_value is stored as settings_value
        query_data["__ruleset_value"] = self.github_settings_value

        # Get the rules for the specified branch
        rules = query_data.get("rules", [])

        # Check if the rule is checked in the ruleset
        rule_enabled = False
        ruleset = None
        for rule in rules:
            # If the rule is present, it is checked
            if self.get_configuration_value_func(rule):
                rule_enabled = True
                # Get the ruleset associated with the rule
                ruleset = rule["ruleset"]
                break

        # If rule is active and we want it enabled,
        # or rule is inactive and we want it disabled,
        # return success.
        if rule_enabled == expected_rule_enabled:
            context = (
                f"{self.github_settings_value} is enabled in Ruleset '{ruleset['name']}'"
                if expected_rule_enabled
                else f"{self.github_settings_value} is disabled"
            )
            return self.EvaluateImplResult(
                EvaluateResult.Success,
                context,
            )

        # When rule is active but we want it disabled
        if rule_enabled:
            assert expected_rule_enabled is False

            return self.EvaluateImplResult(
                EvaluateResult.Error,
                f"{self.github_settings_value} rule active in ruleset '{ruleset['name']}'. It should be set to {expected_rule_enabled}",
                provide_resolution=True,
                provide_rationale=provide_rationale,
            )

        # Rule is inactive but we want it on
        assert rule_enabled is False
        assert expected_rule_enabled is True

        return self.EvaluateImplResult(
            EvaluateResult.Error,
            f"No active branch ruleset with {self.github_settings_value} found",
            provide_resolution=True,
            provide_rationale=provide_rationale,
        )
