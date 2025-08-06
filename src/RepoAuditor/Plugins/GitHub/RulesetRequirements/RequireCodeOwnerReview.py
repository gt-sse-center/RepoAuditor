# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireCodeOwnerReviewRule object."""

import textwrap
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


# ----------------------------------------------------------------------
class RequireCodeOwnerReviewRule(EnableRulesetRequirementImpl):
    """Rule to require a review on a pull request from a designated code owner."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            name="RequireCodeOwnerReviewRule",
            enabled_by_default=False,
            dynamic_arg_name="yes",
            github_ruleset_type="require_code_owner_review",
            github_ruleset_value="Require a pull request before merging -> Require review from Code Owners",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to not require explicit approval from a Code Owner.

                Reasons for this Default
                ------------------------
                - Most repositories are not large enough to warrant specialized reviews by people with specific knowledge about different
                  areas of the code.

                Reasons to Override this Default
                --------------------------------
                - You have a large repository with specialized areas of code that require reviews from specific people.

                * Note: consider reducing the barrier to entry for new contributors by simplifying the design and/or adding automated tests that
                  catch common problems before they are introduced into the code base.
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
