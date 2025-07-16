# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for MergeCommitMessage.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.MergeCommitMessage import MergeCommitMessage
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "allow_merge_commit": True,
            "merge_commit_message": "BLANK",
        },
    }


@pytest.fixture
def requirement():
    return MergeCommitMessage()


@pytest.fixture(name="requirement_args")
def requirement_args_fixture():
    return {"value": "BLANK"}


class TestMergeCommitMessage:
    def test_allow_merge_commit_missing(self, requirement, query_data, requirement_args):
        """Test if `allow_merge_commit` is missing"""
        query_data["standard"] = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_allow_merge_commit_none(self, requirement, query_data, requirement_args):
        """Test if `allow_merge_commit` is None"""
        query_data["standard"]["allow_merge_commit"] = None
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Disabled(self, requirement, query_data, requirement_args):
        """Test when merge commits are disabled"""
        query_data["standard"]["allow_merge_commit"] = False
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "Merge commits are not enabled" in result.context

    def test_MissingMergeCommitMessage(self, requirement, query_data, requirement_args):
        """Missing merge_commit_message value"""
        query_data["standard"].pop("merge_commit_message", None)
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Successful(self, requirement, query_data, requirement_args):
        """Test successful with BLANK commit message value"""
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_IncorrectCommitMessage(self, requirement, query_data, requirement_args):
        """With incorrect commit message value"""
        query_data["standard"]["merge_commit_message"] = "BLUR"
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "it is currently set to 'BLUR'" in result.context
