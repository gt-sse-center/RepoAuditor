# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the StandardQuery object.

The API request/response has the following schema:

REQUEST: https://api.github.com/repos/<username>/<repo>
RESPONSE:
{
    "id": <not used>,
    "node_id": <not used>,
    "name": <not used>",
    "full_name": <not used>,
    "private": Private,
    "owner": {
        "login": <not used>,
        "id": <not used>,
        "node_id": <not used>,
        "avatar_url": <not used>,
        "gravatar_id": <not used>,
        "url": <not used>,
        "html_url": <not used>,
        "followers_url": <not used>,
        "following_url": <not used>,
        "gists_url": <not used>,
        "starred_url": <not used>,
        "subscriptions_url": <not used>,
        "organizations_url": <not used>,
        "repos_url": <not used>,
        "events_url": <not used>,
        "received_events_url": <not used>,
        "type": <not used>,
        "site_admin": <not used>
    },
    "html_url": <not used>,
    "description": Description,
    "fork": <not used>,
    "url": <not used>,
    "forks_url": <not used>,
    "keys_url": <not used>,
    "collaborators_url": <not used>,
    "teams_url": <not used>,
    "hooks_url": <not used>,
    "issue_events_url": <not used>,
    "events_url": <not used>,
    "assignees_url": <not used>,
    "branches_url": <not used>,
    "tags_url": <not used>,
    "blobs_url": <not used>,
    "git_tags_url": <not used>,
    "git_refs_url": <not used>,
    "trees_url": <not used>,
    "statuses_url": <not used>,
    "languages_url": <not used>,
    "stargazers_url": <not used>,
    "contributors_url": <not used>,
    "subscribers_url": <not used>,
    "subscription_url": <not used>,
    "commits_url": <not used>,
    "git_commits_url": <not used>,
    "comments_url": <not used>,
    "issue_comment_url": <not used>,
    "contents_url": <not used>,
    "compare_url": <not used>,
    "merges_url": <not used>,
    "archive_url": <not used>,
    "downloads_url": <not used>,
    "issues_url": <not used>,
    "pulls_url": <not used>,
    "milestones_url": <not used>,
    "notifications_url": <not used>,
    "labels_url": <not used>,
    "releases_url": <not used>,
    "deployments_url": <not used>,
    "created_at": <not used>,
    "updated_at": <not used>,
    "pushed_at": <not used>,
    "git_url": <not used>,
    "ssh_url": <not used>,
    "clone_url": <not used>,
    "svn_url": <not used>,
    "homepage": <not used>,
    "size": <not used>,
    "stargazers_count": <not used>,
    "watchers_count": <not used>,
    "language": <not used>,
    "has_issues": SupportIssues,
    "has_projects": SupportProjects,
    "has_downloads": <not used> (No way to set value in GitHub settings),
    "has_wiki": SupportWikis,
    "has_pages": <not used>,
    "has_discussions": SupportDiscussions,
    "forks_count": <not used>,
    "mirror_url": <not used>,
    "archived": <not used>,
    "disabled": <not used>,
    "open_issues_count": <not used>,
    "license": {
        "key": <not used>,
        "name": License,
        "spdx_id": <not used>,
        "url": <not used>,
        "node_id": <not used>
    },
    "allow_forking": <not used> (No way to set value in GitHub settings),
    "is_template": <not used>,
    "web_commit_signoff_required": WebCommitSignoff,
    "topics": <not used>,
    "visibility": Private,
    "forks": <not used>,
    "open_issues": <not used>,
    "watchers": <not used>,
    "default_branch": DefaultBranch,
    "permissions": {
        "admin": <not used>,
        "maintain": <not used>,
        "push": <not used>,
        "triage": <not used>,
        "pull": <not used>
    },
    "temp_clone_token": <not used>,
    "allow_squash_merge": SquashMergeCommit,
    "allow_merge_commit": MergeCommit,
    "allow_rebase_merge": RebaseMergeCommit,
    "allow_auto_merge": AutoMerge,
    "delete_branch_on_merge": DeleteHeadBranches,
    "allow_update_branch": SuggestUpdatingPullRequestBranches,
    "use_squash_pr_title_as_default": <not used> (No way to set value in GitHub settings),
    "squash_merge_commit_message": SquashMergeCommitMessage,
    "squash_merge_commit_title": <not used> (No way to set value in GitHub settings),
    "merge_commit_message": MergeCommitMessage,
    "merge_commit_title": <not used> (No way to set value in GitHub settings),
    "custom_properties": <not used>,
    "organization": {
        "login": <not used>,
        "id": <not used>,
        "node_id": <not used>,
        "avatar_url": <not used>,
        "gravatar_id": <not used>,
        "url": <not used>,
        "html_url": <not used>,
        "followers_url": <not used>,
        "following_url": <not used>,
        "gists_url": <not used>,
        "starred_url": <not used>,
        "subscriptions_url": <not used>,
        "organizations_url": <not used>,
        "repos_url": <not used>,
        "events_url": <not used>,
        "received_events_url": <not used>,
        "type": <not used>,
        "site_admin": <not used>
    },
    "security_and_analysis": {
        "secret_scanning": SecretScanning,
        "secret_scanning_push_protection": SecretScanningPushProtection,
        "dependabot_security_updates": DependabotSecurityUpdates,
        "secret_scanning_validity_checks": <not used> (The functionality doesn't seem to be available in the UX yet (https://github.blog/2023-10-04-introducing-secret-scanning-validity-checks-for-major-cloud-services/))
    },
    "network_count": <not used>,
    "subscribers_count": <not used>
}
"""

from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Plugins.GitHub.StandardRequirements.AutoMerge import AutoMerge
from RepoAuditor.Plugins.GitHub.StandardRequirements.DefaultBranch import DefaultBranch
from RepoAuditor.Plugins.GitHub.StandardRequirements.DeleteHeadBranches import DeleteHeadBranches
from RepoAuditor.Plugins.GitHub.StandardRequirements.DependabotSecurityUpdates import (
    DependabotSecurityUpdates,
)
from RepoAuditor.Plugins.GitHub.StandardRequirements.Description import Description
from RepoAuditor.Plugins.GitHub.StandardRequirements.License import License
from RepoAuditor.Plugins.GitHub.StandardRequirements.MergeCommit import MergeCommit
from RepoAuditor.Plugins.GitHub.StandardRequirements.MergeCommitMessage import MergeCommitMessage
from RepoAuditor.Plugins.GitHub.StandardRequirements.Private import Private
from RepoAuditor.Plugins.GitHub.StandardRequirements.RebaseMergeCommit import RebaseMergeCommit
from RepoAuditor.Plugins.GitHub.StandardRequirements.SecretScanning import SecretScanning
from RepoAuditor.Plugins.GitHub.StandardRequirements.SecretScanningPushProtection import (
    SecretScanningPushProtection,
)
from RepoAuditor.Plugins.GitHub.StandardRequirements.SquashCommitMerge import SquashCommitMerge
from RepoAuditor.Plugins.GitHub.StandardRequirements.SquashMergeCommitMessage import (
    SquashMergeCommitMessage,
)
from RepoAuditor.Plugins.GitHub.StandardRequirements.SuggestUpdatingPullRequestBranches import (
    SuggestUpdatingPullRequestBranches,
)
from RepoAuditor.Plugins.GitHub.StandardRequirements.SupportDiscussions import SupportDiscussions
from RepoAuditor.Plugins.GitHub.StandardRequirements.SupportIssues import SupportIssues
from RepoAuditor.Plugins.GitHub.StandardRequirements.SupportProjects import SupportProjects
from RepoAuditor.Plugins.GitHub.StandardRequirements.SupportWikis import SupportWikis
from RepoAuditor.Plugins.GitHub.StandardRequirements.TemplateRepository import TemplateRepository
from RepoAuditor.Plugins.GitHub.StandardRequirements.WebCommitSignoff import WebCommitSignoff
from RepoAuditor.Query import ExecutionStyle, Query


# ----------------------------------------------------------------------
class StandardQuery(Query):
    """Query with requirements that operate on basic GitHub repository data."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "StandardQuery",
            ExecutionStyle.Parallel,
            [
                AutoMerge(),
                DefaultBranch(),
                DeleteHeadBranches(),
                Description(),
                DependabotSecurityUpdates(),
                License(),
                MergeCommit(),
                MergeCommitMessage(),
                Private(),
                RebaseMergeCommit(),
                SecretScanning(),
                SecretScanningPushProtection(),
                SquashCommitMerge(),
                SquashMergeCommitMessage(),
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
        """Get the data from an API session."""
        response = module_data["session"].get("")

        response.raise_for_status()
        response = response.json()

        module_data["standard"] = response

        return module_data
