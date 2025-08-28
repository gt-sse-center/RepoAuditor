# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ScientificSoftwareQuery object."""

from RepoAuditor.Plugins.CommunityStandards.CommunityStandardsQuery import CloneRepositoryMixin
from RepoAuditor.Plugins.ScientificSoftware.Requirements.Citation import Citation
from RepoAuditor.Query import ExecutionStyle, Query


class ScientificSoftwareQuery(CloneRepositoryMixin, Query):
    """Query with requirements that check the repository for Scientific Software specific files."""

    def __init__(self) -> None:
        super().__init__(
            "ScientificSoftwareQuery",
            ExecutionStyle.Parallel,
            [
                Citation(),
            ],
        )
