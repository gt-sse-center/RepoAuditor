# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the TemplateRepository object"""

import textwrap

from .Impl.StandardEnableRequirementImpl import StandardEnableRequirementImpl


# ----------------------------------------------------------------------
class TemplateRepository(StandardEnableRequirementImpl):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self):
        super(TemplateRepository, self).__init__(
            "TemplateRepository",
            False,
            "true",
            "settings",
            "General",
            "Template repository",
            lambda data: data["standard"].get("is_template", None),
            rationale=textwrap.dedent(
                """\
                The default behavior is that this is not a template repository.

                Reasons for this Default
                ------------------------
                - Most repositories are not templates.

                Reasons to Override this Default
                --------------------------------
                - Your repository is a template repository.
                """,
            ),
        )
