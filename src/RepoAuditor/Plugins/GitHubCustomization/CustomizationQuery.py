# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CustomizationQuery object."""

from RepoAuditor.Query import ExecutionStyle, Query


class CustomizationQuery(Query):
    """Query with requirements that check for GitHub customization files."""

    def __init__(self) -> None:
        super().__init__(
            "CustomizationQuery",
            ExecutionStyle.Parallel,
            [],  # Empty requirements list for now
        )
