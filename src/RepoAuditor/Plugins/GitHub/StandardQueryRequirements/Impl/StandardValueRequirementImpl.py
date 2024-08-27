# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the StandardValueRequirementImpl object"""

import textwrap

from typing import Any, Callable, Optional

from ...Impl.ValueRequirementImpl import DoesNotApplyResult, ValueRequirementImpl


# ----------------------------------------------------------------------
class StandardValueRequirementImpl(
    ValueRequirementImpl,
):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        default_value: str,
        github_settings_url_suffix: str,
        github_settings_section: Optional[str],
        github_settings_value: Optional[str],
        get_configuration_value_func: Callable[[dict[str, Any]], str | DoesNotApplyResult | None],
        rationale: str,
        subject: Optional[str] = None,
        *,
        requires_explicit_include: bool = False,
    ) -> None:
        if github_settings_section is None:
            resolution = "No Resolution Instructions are available."
        else:
            if github_settings_value is None:
                github_settings_value_display = "the entity"
            else:
                github_settings_value_display = f"'{github_settings_value}'"

            resolution = textwrap.dedent(
                f"""\
                1) Visit '{{session.github_url}}/{github_settings_url_suffix}'
                2) Locate the '{github_settings_section}' section
                3) Ensure that {github_settings_value_display} is set to {{__expected_value}}
                """,
            )

        super(StandardValueRequirementImpl, self).__init__(
            name,
            default_value,
            github_settings_value,
            get_configuration_value_func,
            resolution,
            rationale,
            subject,
            requires_explicit_include=requires_explicit_include,
        )
