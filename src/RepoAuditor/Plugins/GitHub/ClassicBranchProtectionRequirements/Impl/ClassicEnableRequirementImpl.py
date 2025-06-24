# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ClassicEnableRequirementImpl object."""

import textwrap
from collections.abc import Callable
from typing import Any, Optional

from RepoAuditor.Plugins.GitHub.Impl.EnableRequirementImpl import EnableRequirementImpl


# ----------------------------------------------------------------------
class ClassicEnableRequirementImpl(EnableRequirementImpl):
    """Implementation of a requirement that checks a classical setting is enabled."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        enabled_by_default: bool,  # noqa: FBT001
        dynamic_arg_name: str,
        github_settings_section: str,
        github_settings_value: str,
        get_configuration_value_func: Callable[[dict[str, Any]], Optional[bool]],
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        unset_set_terminology: tuple[str, str] = ("unchecked", "checked"),
    ) -> None:
        super().__init__(
            name,
            enabled_by_default,
            dynamic_arg_name,
            github_settings_value,
            get_configuration_value_func,
            textwrap.dedent(
                f"""\
                1) Visit '{{session.github_url}}/settings/branches'
                2) Locate the 'Branch protection rules' section
                3) Click the 'Edit' button next to the branch '{{branch}}'
                4) Locate the '{github_settings_section}' section
                5) Ensure that '{github_settings_value}' is {{__checked_desc}}
                """,
            ),
            rationale,
            subject,
            requires_explicit_include=requires_explicit_include,
            unset_set_terminology=unset_set_terminology,
            missing_value_is_warning=False,
        )
