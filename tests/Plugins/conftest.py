# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Common test fixtures for Plugins"""

from pathlib import Path

import pytest
from utilities import CheckPATFileExists, GetGithubUrl

from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession


@pytest.fixture
def module_data():
    return {
        "session": _GitHubSession("https://github.com/gt-sse-center/RepoAuditor", "pat"),
        "url": "https://github.com/gt-sse-center/RepoAuditor",
    }


# ----------------------------------------------------------------------
@pytest.fixture
def args(request) -> list[str]:
    plugin_name = request.module.__name__.split("_")[0]
    return [
        "--include",
        plugin_name,
        f"--{plugin_name}-url",
        GetGithubUrl(),
    ]


# ----------------------------------------------------------------------
@pytest.fixture
def pat_args(request, args) -> list[str]:
    _github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()
    CheckPATFileExists(_github_pat_filename)

    with _github_pat_filename.open() as f:
        pat_value = f.read().strip()

    plugin_name = request.module.__name__.split("_")[0]
    return args + [f"--{plugin_name}-pat", pat_value]
