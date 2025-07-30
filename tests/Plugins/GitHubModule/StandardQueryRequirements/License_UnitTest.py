# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for License.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.License import License
from RepoAuditor.Requirement import EvaluateResult


@pytest.fixture
def query_data(session):
    return {
        "session": session,
        "standard": {
            "license": {
                "name": "MIT License",
            },
        },
    }


@pytest.fixture
def requirement():
    return License()


class TestLicense:
    def test_license_missing(self, requirement, query_data):
        """Check if no "license" key in query_data
        We should get a `IncompleteDataResult`.
        """
        query_data["standard"] = {}
        result = requirement.Evaluate(
            query_data,
            requirement_args={},
        )
        assert result.result == EvaluateResult.Warning
        assert "Incomplete data was encountered" in result.context

    def test_Empty(self, requirement, query_data):
        """Check if no data under key "license",
        in which case the license value is returned as the empty string.
        """
        query_data["standard"]["license"] = None
        result = requirement.Evaluate(
            query_data,
            requirement_args={},
        )
        assert result.result == EvaluateResult.Error
        assert "'License' must be set to 'MIT License' (it is currently set to '')." in result.context

    def test_Succesful(self, requirement, query_data):
        """Test successful"""
        result = requirement.Evaluate(
            query_data,
            requirement_args={},
        )
        assert result.result == EvaluateResult.Success
