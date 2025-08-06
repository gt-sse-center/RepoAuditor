# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the DismissStalePullRequestApprovalsRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class DismissStalePullRequestApprovalsRule(EnableRulesetRequirementImpl):
    """Rule to dismiss stale pull request approvals when new commits are pushed."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="DismissStalePullRequestApprovalsRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="dismiss_stale_reviews_on_push",
            github_ruleset_value="Require a pull request before merging -> Dismiss stale pull request approvals when new commits are pushed",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to dismiss stale pull request approvals when new commits are pushed.

                Reasons for this Default
                ------------------------
                - Approvals apply to the changes as they existed when the approval was granted. The approval
                  may no longer be valid when new changes are pushed.

                Reasons to Override this Default
                --------------------------------
                You trust the contributor to only make minor changes after approval.
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
        if rule_type is None:
            return None

        if rule_type == "pull_request":
            return rule["parameters"].get(self.github_ruleset_type, False)

        return False
