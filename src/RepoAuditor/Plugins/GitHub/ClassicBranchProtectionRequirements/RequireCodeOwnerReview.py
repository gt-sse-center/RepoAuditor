# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequireCodeOwnerReview object"""

import textwrap

from typing import Any

from .Impl.ClassicEnableRequirementImpl import ClassicEnableRequirementImpl


# ----------------------------------------------------------------------
class RequireCodeOwnerReview(ClassicEnableRequirementImpl):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(RequireCodeOwnerReview, self).__init__(
            "RequireCodeOwnerReview",
            False,
            "true",
            "Protect matching branches",
            "Require a pull request before merging -> Require review from Code Owners",
            _GetValue,
            textwrap.dedent(
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
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetValue(
    data: dict[str, Any],
) -> bool | None:
    settings = data["branch_protection_data"].get("required_pull_request_reviews", None)
    if settings is None:
        return None

    return settings["require_code_owner_reviews"]
