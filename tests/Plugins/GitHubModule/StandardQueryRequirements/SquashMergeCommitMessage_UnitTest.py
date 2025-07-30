# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for SquashMergeCommitMessage.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.SquashMergeCommitMessage import (
    SquashMergeCommitMessage,
)
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "allow_squash_merge": True,
            "squash_merge_commit_message": "COMMIT_MESSAGES",
        },
    }


@pytest.fixture
def requirement():
    return SquashMergeCommitMessage()


class TestSquashMergeCommitMessage:
    def test_allow_merge_commit_missing(self, requirement, query_data):
        """Test if `allow_merge_commit` is missing"""
        query_data["standard"] = {}
        requirement_args = {}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Disabled(self, requirement, query_data):
        """Test when squash merges are disabled"""
        query_data["standard"]["allow_squash_merge"] = False
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply
        assert "Squash merge commits are not enabled." in result.context

    def test_MissingValue(self, requirement, query_data):
        """Missing squash_merge_commit_message value"""
        query_data["standard"]["allow_squash_merge"] = True
        query_data["standard"].pop("squash_merge_commit_message", None)

        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_CommitMessage(self, requirement, query_data):
        """With COMMIT_MESSAGES squash-merge commit message value"""
        query_data["standard"]["squash_merge_commit_message"] = "COMMIT_MESSAGES"
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success

    def test_IncorrectValue(self, requirement, query_data):
        """With incorrect commit message value"""
        query_data["standard"]["squash_merge_commit_message"] = "NO_COMMIT_MESSAGES"
        requirement_args = {"value": "COMMIT_MESSAGES"}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "it is currently set to 'NO_COMMIT_MESSAGES'" in result.context
