# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Common fixtures for GitHubModule unit tests."""

import pytest
from dataclasses import dataclass


@pytest.fixture
def session():
    """Create a dummy GitHub API session object."""

    @dataclass(frozen=True)
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
