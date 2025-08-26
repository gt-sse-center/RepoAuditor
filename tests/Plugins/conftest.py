# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Common test fixtures for Plugins."""

from pathlib import Path
from typing import Any

import pytest

# Fixtures included here so it is available for all tests
from GitHubModule.fixtures import query_data_fixture, session_fixture  # noqa: F401
from utilities import CheckPATFileExists, GetGithubUrl

from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession


@pytest.fixture
def module_data() -> dict[str, Any]:
    """Get the data required by the module."""
    return {
        "session": _GitHubSession("https://github.com/gt-sse-center/RepoAuditor", "pat"),
        "url": "https://github.com/gt-sse-center/RepoAuditor",
    }


# ----------------------------------------------------------------------
@pytest.fixture(name="args")
def args_fixture(request) -> list[str]:
    """Fixture for the command line arguments.
    `request` is a fixture representing the object
    which is requesting this fixture.
    """
    # Get the plugin name from the requesting test.
    plugin_name = request.module.__name__.split("_")[0]
    return [
        "--include",
        plugin_name,
        f"--{plugin_name}-url",
        GetGithubUrl(),
    ]


# ----------------------------------------------------------------------
@pytest.fixture(name="pat_args")
def pat_args_fixture(request, args: list[str]) -> list[str]:
    """Fixture for the PAT along with the command line arguments.

    `request` is a fixture representing the object
    which is requesting this fixture.
    """
    github_pat_filename = (Path(__file__).parent / "github_pat.txt").resolve()
    CheckPATFileExists(github_pat_filename)

    plugin_name = request.module.__name__.split("_")[0]
    return [*args, f"--{plugin_name}-pat", str(github_pat_filename)]
