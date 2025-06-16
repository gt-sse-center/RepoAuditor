# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Common fixtures for GitHubModule unit tests."""

import pytest


@pytest.fixture
def session():
    """Create a dummy GitHub API session object."""

    class _GithubSession_:
        pass

    s = _GithubSession_()
    s.github_url = "https://github.com/gt-sse-center/RepoAuditor"
    s.pat = "dummy_github_pat.txt"
    return s
