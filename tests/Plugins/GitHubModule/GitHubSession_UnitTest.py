# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHubSession"""

from pathlib import Path

import pytest
import requests

from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession


@pytest.fixture
def github_pat(fs):
    """Fixture for GitHub PAT file, which creates a fake PAT file and returns the path."""
    pat_path = Path(__file__).parent / "dummy_github_pat.txt"
    fs.create_file(pat_path, contents="github_path_abcdefghijklmnop")
    return pat_path


def mock_request(
    self,
    method,
    url,
    *args,
    **kwargs,
):
    """Mocked request function."""
    r = requests.Response()
    r.status_code = 200
    r.method = method
    r.url = url
    return r


class TestGitHubSession:
    """Unit tests for the _GitHubSession class."""

    @classmethod
    def setup_class(cls):
        """Setup values for each test."""
        cls.github_url = "https://github.com/gt-sse-center/RepoAuditor"

    def test_Construct(self, github_pat):
        """Test constructor."""
        session = _GitHubSession(github_url=self.github_url, github_pat=github_pat)

        assert session.github_url == self.github_url

    def test_ConstructTrailingSlash(self, github_pat):
        """Test with trailing slash for URL."""
        session = _GitHubSession(github_url=self.github_url + "/", github_pat=github_pat)

        assert session.github_url == self.github_url

    def test_InvalidRepository(self, github_pat):
        """Test with invalid repository URL."""
        with pytest.raises(ValueError):
            _GitHubSession(
                github_url="https://github.com/gt-sse-center/RepoAuditor/123", github_pat=github_pat
            )

    def test_EnterpriseUrl(self, github_pat):
        """Test with enterprise URL."""
        github_enterprise_url = "https://github.gatech.edu/gt-sse-center/RepoAuditor"
        session = _GitHubSession(github_url=github_enterprise_url, github_pat=github_pat)
        assert session.github_url == github_enterprise_url

    def test_Request(self, github_pat, monkeypatch):
        """Test the _GitHubSession.request method."""
        session = _GitHubSession(github_url=self.github_url, github_pat=github_pat)

        monkeypatch.setattr(requests.Session, "request", mock_request)
        r = session.request("GET", "test")

        assert r.url == "https://api.github.com/repos/gt-sse-center/RepoAuditor/test"

    def test_RequestLeadingSlash(self, github_pat, monkeypatch):
        """Test the _GitHubSession.request method."""
        session = _GitHubSession(github_url=self.github_url, github_pat=github_pat)

        monkeypatch.setattr(requests.Session, "request", mock_request)
        r = session.request("GET", "/test")

        assert r.url == "https://api.github.com/repos/gt-sse-center/RepoAuditor/test"
