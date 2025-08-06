# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the EnsureStatusChecksRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class EnsureStatusChecksRule(EnableRulesetRequirementImpl):
    """Rule to verify status checks have been assigned as a rule for a branch."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="EnsureStatusChecksRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="required_status_checks",
            github_ruleset_value="Require status checks to pass -> Status checks that are required",
            get_configuration_value_func=self._GetValue,
            resolution=textwrap.dedent(
                """\
                1) Visit '{session.github_url}/settings/rules'.
                2) Find or create a ruleset on the branch '{branch}'.
                3) Go to '{__ruleset_value}'.
                4) Click on '+ Add checks'.
                5) Type the name of the check to enforce.
                6) Select status checks that must pass before merging.
                """,
            ),
            rationale=textwrap.dedent(
                """\
                The default behavior is to require the specification of at least one status check that must pass before merging.

                Reasons for this Default
                ------------------------
                - A Continuous Integration process must be gated by some activity, action, or work flow.

                Reasons to Override this Default
                --------------------------------
                - Code reviews are sufficient to ensure the quality of pull requests before they are merged into the branch
                  (this is not recommended).
                """
            ),
        )

    # ----------------------------------------------------------------------
    @override
    def _GetValue(
        self,
        rule: dict[str, Any],
    ) -> Optional[bool]:
        rule_type = rule.get("type")

        # If rule_type doesn't exist,
        # it means the rule is not applicable
        if rule_type and rule_type == self.github_ruleset_type:
            return len(rule["parameters"][self.github_ruleset_type]) > 0

        return False
