# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ClassicValueRequirementImpl object."""

import textwrap
from collections.abc import Callable
from typing import Any, Optional

from RepoAuditor.Plugins.GitHub.Impl.ValueRequirementImpl import DoesNotApplyResult, ValueRequirementImpl


# ----------------------------------------------------------------------
class ClassicValueRequirementImpl(ValueRequirementImpl):
    """Implementation of a requirement that checks a classic value in GitHub settings."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        default_value: str,
        github_settings_section: Optional[str],
        github_settings_value: Optional[str],
        get_configuration_value_func: Callable[[dict[str, Any]], str | DoesNotApplyResult | None],
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
    ) -> None:
        if github_settings_section is None:
            resolution = "No resolution instructions are available"
        else:
            if github_settings_value is None:
                github_settings_value_display = "the entity"
            else:
                github_settings_value_display = f"'{github_settings_value}'"

            resolution = textwrap.dedent(
                f"""\
                1) Visit '{{session.github_url}}/settings/branches'.
                2) Locate the 'Branch protection rules' section.
                3) Click the 'Edit' button next to the branch '{{branch}}'.
                4) Locate the '{github_settings_section}' section.
                5) Ensure that {github_settings_value_display} is '{{__expected_value}}'.
                """,
            )

        super().__init__(
            name,
            default_value,
            github_settings_value,
            get_configuration_value_func,
            resolution,
            rationale,
            subject,
            requires_explicit_include=requires_explicit_include,
            missing_value_is_warning=False,
        )
