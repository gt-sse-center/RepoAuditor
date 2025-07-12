# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for CommunityStandardsQuery.py"""

import pytest
from git import Repo

from RepoAuditor.Plugins.CommunityStandards.CommunityStandardsQuery import (
    CommunityStandardsQuery,
    TemporaryDirectory,
)


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

        def mock_clone_from(github_url, repo_dirname, branch="main"):
            """A mocked clone_from method for the git.Repo class."""
            pass

        monkeypatch.setattr(
            Repo,
            "clone_from",
            mock_clone_from,
        )

        query = CommunityStandardsQuery()
        query_data = query.GetData(module_data)

        assert query_data["repo_dir"].name == "test_temp_directory"

    def test_GetData_adds_pat(self, module_data, monkeypatch):
        """Test the GetData method adds PAT to URL"""
        github_pat = "pat-123"
        github_url = "https://github.com/owner/repo"
        expected_url = "https://pat-123@github.com/owner/repo"
        module_data["url"] = github_url
        module_data["pat"] = github_pat

        monkeypatch.setattr(
            TemporaryDirectory,
            "__init__",
            MockTemporaryDirectory.__init__,
        )

        def mock_clone_from(github_url, repo_dirname, branch="main"):
            assert github_url == expected_url

        monkeypatch.setattr(Repo, "clone_from", mock_clone_from)

        query = CommunityStandardsQuery()
        _ = query.GetData(module_data)

    def test_GetData_does_not_add_pat(self, module_data, monkeypatch):
        """Test the GetData method preserves the URL when no PAT is provided"""
        github_url = "https://github.com/owner/repo"
        expected_url = "https://github.com/owner/repo"
        module_data["url"] = github_url

        monkeypatch.setattr(
            TemporaryDirectory,
            "__init__",
            MockTemporaryDirectory.__init__,
        )

        def mock_clone_from(github_url, repo_dirname, branch="main"):
            assert github_url == expected_url

        monkeypatch.setattr(Repo, "clone_from", mock_clone_from)

        query = CommunityStandardsQuery()
        _ = query.GetData(module_data)

    def test_GetData_handles_gitpython_errors(self, module_data, monkeypatch):
        """Test the GetData method handles errors raised by the gitpyhon module"""
        gitpython_error_msg = "error cloning repository"

        monkeypatch.setattr(
            TemporaryDirectory,
            "__init__",
            MockTemporaryDirectory.__init__,
        )

        def mock_clone_from(github_url, repo_dirname, branch="main"):
            raise Exception(gitpython_error_msg)

        monkeypatch.setattr(Repo, "clone_from", mock_clone_from)

        query = CommunityStandardsQuery()
        with pytest.raises(RuntimeError) as e_info:
            _ = query.GetData(module_data)
        assert gitpython_error_msg in str(e_info)

    def test_Cleanup(self, module_data):
        """Test the Cleanup method."""
        query = CommunityStandardsQuery()
        module_data["repo_dir"] = MockTemporaryDirectory()
        result = query.Cleanup(module_data)

        assert result is None
