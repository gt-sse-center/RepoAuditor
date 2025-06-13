# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHubSession"""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase as FakeFSTestCase

from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession


class TestGitHubSession(FakeFSTestCase):
    """Unit tests for the _GitHubSession class."""

    def setUp(self):
        self.setUpPyfakefs()

    def test_Construct(self):
        """Test constructor."""
        github_url = "https://github.com/gt-sse-center/RepoAuditor"

        github_pat = Path(__file__).parent / "dummy_github_pat.txt"
        self.fs.create_file(github_pat, contents="github_path_abcdefghijklmnop")

        session = _GitHubSession(github_url=github_url, github_pat=github_pat)

        assert session.github_url == github_url

        # Test with trailing slash for URL
        session = _GitHubSession(github_url=github_url + "/", github_pat=github_pat)

        assert session.github_url == github_url

        # Test with invalid repository
        with pytest.raises(ValueError):
            session = _GitHubSession(
                github_url="https://github.com/gt-sse-center/RepoAuditor/123", github_pat=github_pat
            )

        # Test with enterprise URL
        github_enterprise_url = "https://github.gatech.edu/gt-sse-center/RepoAuditor"
        session = _GitHubSession(github_url=github_enterprise_url, github_pat=github_pat)
        assert session.github_url == github_enterprise_url
