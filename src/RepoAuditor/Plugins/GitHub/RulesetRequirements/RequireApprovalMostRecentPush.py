# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireApprovalMostRecentPushRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class RequireApprovalMostRecentPushRule(EnableRulesetRequirementImpl):
    """Rule to require approval on the most recent reviewable push in a pull request."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="RequireApprovalMostRecentPushRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="require_last_push_approval",
            github_ruleset_value="Require a pull request before merging -> Require approval of the most recent reviewable push",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to require approval of the most recent reviewable push by someone other than the author of the pull request.

                Reasons for this Default
                ------------------------
                - Self-approval of a pull request eliminates the value provided by a second pair of eyes during a code review.

                Reasons to Override this Default
                --------------------------------
                - You are the only person working on the repository.
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

        if rule_type == "pull_request":
            return rule["parameters"].get(self.github_ruleset_type, False)

        return False
