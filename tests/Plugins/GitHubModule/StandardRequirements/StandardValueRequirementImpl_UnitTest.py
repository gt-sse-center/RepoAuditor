# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for StandardValueRequirementImpl.py"""

import pytest

from RepoAuditor.Plugins.GitHub.StandardRequirements.Impl.StandardValueRequirementImpl import (
    StandardValueRequirementImpl,
)
from RepoAuditor.Requirement import EvaluateResult


class TestStandardValueRequirementImpl:
    """Tests for the StandardValueRequirementImpl requirement class."""

    def test_no_github_settings_section(self, query_data):
        """Test if `github_settings_section` is missing."""
        requirement = StandardValueRequirementImpl(
            name="Test",
            default_value="enabled",
            github_settings_url_suffix="/repos/RepoAuditor",
            github_settings_section=None,
            github_settings_value="Setting",
            get_configuration_value_func=lambda x: x["value"],
            rationale="Rationale",
        )
        query_data["value"] = "test result"
        requirement_args = {"value": "result"}

        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "No Resolution Instructions are available." in result.resolution

    def test_no_github_settings_value(self, query_data):
        """Test if `github_settings_value` is missing."""
        requirement = StandardValueRequirementImpl(
            name="Test",
            default_value="enabled",
            github_settings_url_suffix="/repos/RepoAuditor",
            github_settings_section="Section",
            github_settings_value=None,
            get_configuration_value_func=lambda x: x["value"],
            rationale="Rationale",
        )
        query_data["value"] = "test result"
        requirement_args = {"value": "result"}

        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "Ensure that the entity" in result.resolution
