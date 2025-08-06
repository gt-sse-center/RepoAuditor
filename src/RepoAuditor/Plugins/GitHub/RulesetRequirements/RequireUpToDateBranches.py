# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireUpToDateBranchesRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class RequireUpToDateBranchesRule(EnableRulesetRequirementImpl):
    """Rule to require branches be up to date with latest code for status checks to run."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="RequireUpToDateBranchesRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="strict_required_status_checks_policy",
            github_ruleset_value="Require status checks to pass -> Require branches to be up to date before merging",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to require branches to be up to date before merging. The terminology
                used by GitHub is a bit confusing, as this setting ensures that all GitHub workflows triggered
                by the pull request have completed successfully before the pull request can be merged.

                Reasons for this Default
                ------------------------
                - Workflows run should pass before a pull request is merged into the mainline branch.

                Reasons to Override this Default
                --------------------------------
                <unknown>
                """,
            ),
        )

    # ----------------------------------------------------------------------
    @override
    def _GetValue(
        self,
        rule: dict[str, Any],
    ) -> Optional[bool]:
        rule_type = rule.get("type")
        if rule_type is None:
            return None

        if rule_type == "required_status_checks":
            return rule["parameters"].get("strict_required_status_checks_policy", False)

        return False
