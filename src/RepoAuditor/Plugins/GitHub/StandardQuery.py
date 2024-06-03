# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the StandardQuery object"""

from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Query import ExecutionStyle, Query

from .StandardQueryRequirements.AutoMerge import AutoMerge
from .StandardQueryRequirements.DeleteHeadBranches import DeleteHeadBranches
from .StandardQueryRequirements.DependabotSecurityUpdates import DependabotSecurityUpdates
from .StandardQueryRequirements.MergeCommit import MergeCommit
from .StandardQueryRequirements.RebaseMergeCommit import RebaseMergeCommit
from .StandardQueryRequirements.SecretScanning import SecretScanning
from .StandardQueryRequirements.SecretScanningPushProtection import SecretScanningPushProtection
from .StandardQueryRequirements.SquashCommitMerge import SquashCommitMerge
from .StandardQueryRequirements.SuggestUpdatingPullRequestBranches import (
    SuggestUpdatingPullRequestBranches,
)
from .StandardQueryRequirements.SupportDiscussions import SupportDiscussions
from .StandardQueryRequirements.SupportIssues import SupportIssues
from .StandardQueryRequirements.SupportProjects import SupportProjects
from .StandardQueryRequirements.SupportWikis import SupportWikis
from .StandardQueryRequirements.TemplateRepository import TemplateRepository
from .StandardQueryRequirements.WebCommitSignoff import WebCommitSignoff


# ----------------------------------------------------------------------
class StandardQuery(Query):
    """Query with requirements that operate on basic GitHub repository data."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super(StandardQuery, self).__init__(
            "StandardQuery",
            ExecutionStyle.Parallel,
            [
                AutoMerge(),
                DeleteHeadBranches(),
                DependabotSecurityUpdates(),
                MergeCommit(),
                RebaseMergeCommit(),
                SecretScanning(),
                SecretScanningPushProtection(),
                SquashCommitMerge(),
                SuggestUpdatingPullRequestBranches(),
                SupportDiscussions(),
                SupportIssues(),
                SupportProjects(),
                SupportWikis(),
                TemplateRepository(),
                WebCommitSignoff(),
            ],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        response = module_data["session"].get("")

        response.raise_for_status()
        response = response.json()

        module_data["standard"] = response

        return module_data
