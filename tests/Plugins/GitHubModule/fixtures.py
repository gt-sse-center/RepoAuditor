# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""
Common fixtures for GitHubModule unit tests.
The fixtures here are imported within the top-level conftest.py so that they are accessible everywhere.
"""

import pytest
from dataclasses import dataclass


@pytest.fixture(name="session")
def session_fixture():
    """Create a dummy GitHub API session object."""

    @dataclass
    class _GithubSession_:
        github_url: str
        pat: str
        is_enterprise: bool

    s = _GithubSession_(
        "https://github.com/gt-sse-center/RepoAuditor",
        pat="github_pat_dummy",
        is_enterprise=False,
    )
    return s


@pytest.fixture(name="query_data")
def query_data_fixture(session):
    return {
        "session": session,
        "branch": "main",
        "branch_protection_data": {
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_last_push_approval": True,
                "required_approving_review_count": "1",
                "require_code_owner_reviews": False,
            },
            "required_status_checks": {
                "checks": ["check1", "check2"],
                "strict": False,
            },
        },
        "default_branch_data": {
            "protected": True,
        },
        "standard": {
            "description": "Description of repository",
            "allow_merge_commit": True,
            "merge_commit_message": "BLANK",
            "allow_squash_merge": True,
            "squash_merge_commit_message": "COMMIT_MESSAGES",
            "security_and_analysis": {
                "dependabot_security_updates": {
                    "status": True,
                },
                "secret_scanning_push_protection": {
                    "status": True,
                },
                "secret_scanning": {
                    "status": True,
                },
            },
            "private": True,
            "license": {
                "name": "MIT License",
            },
        },
        "pat": "github_pat_abcdefgh",
    }
