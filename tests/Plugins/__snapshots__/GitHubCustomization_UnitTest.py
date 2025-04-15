# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHubCustomization plugin"""

import os
import tempfile
from pathlib import Path

import pytest

from RepoAuditor.Requirement import EvaluateResult
from RepoAuditor.Plugins.GitHubCustomization.Requirements.IssueTemplates import IssueTemplates
from RepoAuditor.Plugins.GitHubCustomization.Requirements.PullRequestTemplate import (
    PullRequestTemplate,
)
from RepoAuditor.Plugins.GitHubCustomization.Requirements.SecurityPolicy import SecurityPolicy
from RepoAuditor.Plugins.GitHubCustomization.Requirements.CodeOwners import CodeOwners
from RepoAuditor.Plugins.GitHubCustomization.Requirements.Contributing import Contributing


# ----------------------------------------------------------------------
class TestGitHubCustomization:
    # ----------------------------------------------------------------------
    @pytest.fixture
    def temp_repo(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    # ----------------------------------------------------------------------
    def test_IssueTemplates_Missing(self, temp_repo):
        requirement = IssueTemplates()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Error
        assert "No issue templates found" in result.context

    # ----------------------------------------------------------------------
    def test_IssueTemplates_Directory(self, temp_repo):
        # Create issue template directory with a template
        template_dir = temp_repo / ".github" / "ISSUE_TEMPLATE"
        template_dir.mkdir(parents=True)

        template_file = template_dir / "bug_report.md"
        template_file.write_text("# Bug Report Template")

        requirement = IssueTemplates()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def test_IssueTemplates_SingleFile(self, temp_repo):
        # Create single issue template file
        github_dir = temp_repo / ".github"
        github_dir.mkdir(parents=True)

        template_file = github_dir / "ISSUE_TEMPLATE.md"
        template_file.write_text("# Issue Template")

        requirement = IssueTemplates()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def test_PullRequestTemplate_Missing(self, temp_repo):
        requirement = PullRequestTemplate()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Error
        assert "No pull request template found" in result.context

    # ----------------------------------------------------------------------
    def test_PullRequestTemplate_GithubDir(self, temp_repo):
        # Create PR template in .github directory
        github_dir = temp_repo / ".github"
        github_dir.mkdir(parents=True)

        template_file = github_dir / "PULL_REQUEST_TEMPLATE.md"
        template_file.write_text("# PR Template")

        requirement = PullRequestTemplate()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def test_PullRequestTemplate_RootDir(self, temp_repo):
        # Create PR template in root directory
        template_file = temp_repo / "PULL_REQUEST_TEMPLATE.md"
        template_file.write_text("# PR Template")

        requirement = PullRequestTemplate()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def test_SecurityPolicy_Missing(self, temp_repo):
        requirement = SecurityPolicy()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Error
        assert "No security policy found" in result.context

    # ----------------------------------------------------------------------
    def test_SecurityPolicy_GithubDir(self, temp_repo):
        # Create security policy in .github directory
        github_dir = temp_repo / ".github"
        github_dir.mkdir(parents=True)

        policy_file = github_dir / "SECURITY.md"
        policy_file.write_text("# Security Policy")

        requirement = SecurityPolicy()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def test_CodeOwners_Missing(self, temp_repo):
        requirement = CodeOwners()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})
        self._debug_result_attributes(result)

        assert result.result == EvaluateResult.Error
        error_message = result.context
        assert "No CODEOWNERS file found" in error_message

    # ----------------------------------------------------------------------
    def test_CodeOwners_GithubDir(self, temp_repo):
        # Create CODEOWNERS in .github directory
        github_dir = temp_repo / ".github"
        github_dir.mkdir(parents=True)

        codeowners_file = github_dir / "CODEOWNERS"
        codeowners_file.write_text("* @owner")

        requirement = CodeOwners()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def test_Contributing_Missing(self, temp_repo):
        requirement = Contributing()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Error
        assert "No contributing guide found" in result.context

    # ----------------------------------------------------------------------
    def test_Contributing_RootDir(self, temp_repo):
        # Create contributing guide in root directory
        contributing_file = temp_repo / "CONTRIBUTING.md"
        contributing_file.write_text("# Contributing Guide")

        requirement = Contributing()
        result = requirement._EvaluateImpl({"repo_path": temp_repo}, {})

        assert result.result == EvaluateResult.Success

    # ----------------------------------------------------------------------
    def _debug_result_attributes(self, result):
        print(f"Result type: {type(result)}")
        print(f"Result attributes: {dir(result)}")
        if hasattr(result, "result"):
            print(f"Result.result: {result.result}")
        for attr in ["description", "message", "error", "error_message"]:
            if hasattr(result, attr):
                print(f"Result.{attr}: {getattr(result, attr)}")
