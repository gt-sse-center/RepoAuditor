# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ClassicBranchProtection object"""

from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Query import ExecutionStyle, Query

from .ClassicBranchProtectionRequirements.DoNotAllowBypassSettings import DoNotAllowBypassSettings


# ----------------------------------------------------------------------
class ClassicBranchProtectionQuery(Query):
    """Query with requirements that operate on class branch protection rules."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super(ClassicBranchProtectionQuery, self).__init__(
            "ClassicBranchProtectionQuery",
            ExecutionStyle.Parallel,
            [
                DoNotAllowBypassSettings(),
            ],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        # Get the default branch name
        response = module_data["session"].get("")

        response.raise_for_status()
        response = response.json()

        module_data["default_branch"] = response["default_branch"]

        # Get the information for the default branch
        response = module_data["session"].get(f"branches/{module_data['default_branch']}")

        response.raise_for_status()
        response = response.json()

        module_data["default_branch_data"] = response

        if not module_data["default_branch_data"].get("protected", False):
            return None

        # Note that once here, we know that the branch is protected, but we don't know the
        # protection scheme used (rulesets or classic). Attempt to get the classic information
        # and then see if rulesets are in use if the classic information is not found.
        response = module_data["session"].get(
            f"/branches/{module_data['default_branch']}/protection"
        )

        if response.status_code == 404:
            # Does this branch use rulesets?
            ruleset_response = module_data["session"].get(
                f"rules/branches/{module_data['default_branch']}"
            )

            ruleset_response.raise_for_status()
            ruleset_response = ruleset_response.json()

            # If there is data, assume that the branch is protected by rulesets
            if ruleset_response:
                return None

            # Classic branch protection information is only accessible when a pat is provided. Exit
            # gracefully if there isn't a PAT, as the DefaultBranchQuery will print a warning if
            # the PAT wasn't provided.
            if module_data["session"].github_pat is None:
                return None

            # If here, let the error result in an exception in the line below.

        response.raise_for_status()
        response = response.json()

        module_data["branch_protection_data"] = response

        return module_data
