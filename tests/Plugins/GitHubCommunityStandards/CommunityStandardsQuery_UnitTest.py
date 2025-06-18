# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for CommunityStandardsQuery.py"""

import pytest
from git import Repo

from RepoAuditor.Plugins.GitHubCommunityStandards.CommunityStandardsQuery import (
    CommunityStandardsQuery,
    TemporaryDirectory,
)


def mock_clone_from(github_url, repo_dirname, branch="main"):
    """A mocked clone_from method for the git.Repo class."""
    pass


class MockTemporaryDirectory:
    """A mock class to replace tempfile.TemporaryDirectory."""

    def __init__(self):
        self.name = "test_temp_directory"

    def cleanup(self):
        """Mocked cleanup method"""


@pytest.fixture(autouse=True)
def patch_temp_directory(monkeypatch):
    monkeypatch.delattr("tempfile.TemporaryDirectory")


class TestCommunityStandardsQuery:
    def test_GetData(self, module_data, monkeypatch):
        """Test the GetData method."""
        monkeypatch.setattr(
            TemporaryDirectory,
            "__init__",
            MockTemporaryDirectory.__init__,
        )
        monkeypatch.setattr(
            Repo,
            "clone_from",
            mock_clone_from,
        )

        query = CommunityStandardsQuery()
        query_data = query.GetData(module_data)

        assert query_data["repo_dir"].name == "test_temp_directory"

    def test_Cleanup(self, module_data):
        """Test the Cleanup method."""
        query = CommunityStandardsQuery()
        module_data["repo_dir"] = MockTemporaryDirectory()
        result = query.Cleanup(module_data)

        assert result is None
