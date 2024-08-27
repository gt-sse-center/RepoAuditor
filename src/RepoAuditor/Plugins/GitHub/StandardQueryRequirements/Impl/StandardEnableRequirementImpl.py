# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the StandardEnableRequirementImpl object"""

import textwrap

from typing import Any, Callable, Optional

from ...Impl.EnableRequirementImpl import EnableRequirementImpl


# ----------------------------------------------------------------------
class StandardEnableRequirementImpl(
    EnableRequirementImpl
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        default_value: bool,
        dynamic_arg_name: str,
        github_settings_url_suffix: str,
        github_settings_section: str,
        github_settings_value: str,
        get_configuration_value_func: Callable[[dict[str, Any]], Optional[bool]],
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
        unset_set_terminology: tuple[str, str] = ("unchecked", "checked"),
    ) -> None:
        super(StandardEnableRequirementImpl, self).__init__(
            name,
            default_value,
            dynamic_arg_name,
            github_settings_value,
            get_configuration_value_func,
            textwrap.dedent(
                f"""\
                1) Visit '{{session.github_url}}/{github_settings_url_suffix}'
                2) Locate the '{github_settings_section}' section
                3) Ensure that {github_settings_value} is {{__checked_desc}}
                """,
            ),
            rationale,
            subject,
            requires_explicit_include=requires_explicit_include,
            unset_set_terminology=unset_set_terminology,
        )
