# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHub/Module.py"""

from pathlib import Path

from RepoAuditor.Plugins.GitHub.Module import GitHubModule
from RepoAuditor.Plugins.GitHubBase.Module import _GitHubSession


class TestGitHubModule:
    """Unit tests for the Module class in the GitHub plugin."""

    def test_Construct(self):
        """Test constructor."""
        module = GitHubModule()
        assert isinstance(module, GitHubModule)

    def test_GenerateInitialData(self):
        """Test GenerateInitialData method."""
        dynamic_args = {
            "url": "https://github.com/gt-sse-center/RepoAuditor",
            "pat": Path(__file__).parent / "dummy_github_pat.txt",
        }
        module = GitHubModule()
        dynamic_args = module.GenerateInitialData(dynamic_args)

        assert "session" in dynamic_args
        assert isinstance(dynamic_args["session"], _GitHubSession)
