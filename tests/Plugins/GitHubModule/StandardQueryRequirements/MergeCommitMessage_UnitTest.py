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


class TestMergeCommitMessage:
    def test_allow_merge_commit_missing(self, requirement, query_data):
        """Test if `allow_merge_commit` is missing"""
        query_data["standard"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_allow_merge_commit_none(self, requirement, query_data):
        """Test if `allow_merge_commit` is None"""
        query_data["standard"]["allow_merge_commit"] = None
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Disabled(self, requirement, query_data):
        """Test when merge commits are disabled"""
        query_data["standard"]["allow_merge_commit"] = False
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "Merge commits are not enabled" in result.context

    def test_MissingMergeCommitMessage(self, requirement, query_data):
        """Missing merge_commit_message value"""
        query_data["standard"].pop("merge_commit_message", None)
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Successful(self, requirement, query_data):
        """Test successful with BLANK commit message value"""
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_IncorrectCommitMessage(self, requirement, query_data):
        """With incorrect commit message value"""
        query_data["standard"]["merge_commit_message"] = "BLUR"
        requirement_args = {"value": "BLANK"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "it is currently set to 'BLUR'" in result.context
