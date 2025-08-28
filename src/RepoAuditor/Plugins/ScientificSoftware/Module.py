# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the ScientificSoftwareModule object."""

from RepoAuditor.Module import ExecutionStyle
from RepoAuditor.Plugins.GitHubBase.Module import GitHubBaseModule
from RepoAuditor.Plugins.ScientificSoftware.ScientificSoftwareQuery import ScientificSoftwareQuery


class ScientificSoftwareModule(GitHubBaseModule):
    """Module that validates existence of repository files for Scientific Software."""

    def __init__(self) -> None:
        super().__init__(
            "ScientificSoftware",
            "Validates existence of repository files for Scientific Software.",
            ExecutionStyle.Parallel,
            [
                ScientificSoftwareQuery(),
            ],
            requires_explicit_include=True,
        )
