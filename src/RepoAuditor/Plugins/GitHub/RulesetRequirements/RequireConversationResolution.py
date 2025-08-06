# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireConversationResolutionRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class RequireConversationResolutionRule(EnableRulesetRequirementImpl):
    """Rule to require all review conversations to be marked as resolved on a pull request."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="RequireConversationResolutionRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="required_review_thread_resolution",
            github_ruleset_value="Require a pull request before merging -> Require conversation resolution before merging",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to require conversation resolution before merging a pull request.

                Reasons for this Default
                ------------------------
                - Conversation resolution is an important part of the development process.
                - Prevent the accidental merging of a pull request before changes associated with the comments have been made.

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

        if rule_type == "pull_request":
            return rule["parameters"].get(self.github_ruleset_type, False)

        return False
