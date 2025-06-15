# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Common test fixtures for Plugins"""

import pytest
from GitHubModule.fixtures import session

from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession


@pytest.fixture
def module_data():
    return {
        "session": _GitHubSession("https://github.com/gt-sse-center/RepoAuditor", "pat"),
        "url": "https://github.com/gt-sse-center/RepoAuditor",
    }
