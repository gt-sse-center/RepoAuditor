# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireApprovalsRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class RequireApprovalsRule(EnableRulesetRequirementImpl):
    """Rule to require at least 1 approval on a pull request."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="RequireApprovalsRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="required_approving_review_count",
            github_ruleset_value="Require a pull request before merging -> Required approvals",
            get_configuration_value_func=self._GetValue,
            resolution=textwrap.dedent(
                """\
                1) Visit '{session.github_url}/settings/rules'.
                2) Find or create a ruleset on the branch '{branch}'.
                3) Go to '{__ruleset_value}'.
                4) Set the number of required approvals to at least 1.
                """
            ),
            rationale=textwrap.dedent(
                """\
                The default behavior is to require at least one approval.

                Reasons for this Default
                ------------------------
                - Code Reviews are a generally accepted best practice for software development.

                Reasons to Override this Default
                --------------------------------
                - You are the only person working on the repository (set the value to 0).
                - You want to require more than one approval (set the value to the number of approvals required).
                - You are not comfortable with the amount of time code reviews introduce in the development process (set the value to 0).
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
            return rule["parameters"].get(self.github_ruleset_type, 0) > 0

        return False
