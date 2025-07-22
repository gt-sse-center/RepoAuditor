# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHub/Impl/ClassicValueRequirementImpl.py"""

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionRequirements.Impl.ClassicValueRequirementImpl import (
    ClassicValueRequirementImpl,
)


class TestClassicValueRequirementImpl:
    def test_SettingsValue(self):
        """Test the ClassicValueRequirementImpl class."""
        requirement = ClassicValueRequirementImpl(
            "Require Some Value",
            "Disabled",
            github_settings_section=None,
            github_settings_value="No Settings Section",
            get_configuration_value_func=lambda _: "yes",
            rationale="For testing",
        )
        assert requirement.github_value == "'No Settings Section'"

    def test_NoSettingsValue(self):
        """Test for when no github_settings_value is provided."""
        requirement = ClassicValueRequirementImpl(
            "Require Some Value",
            "Disabled",
            github_settings_section="Protect funky feature",
            github_settings_value=None,
            get_configuration_value_func=lambda _: "yes",
            rationale="For testing",
        )
        assert requirement.github_value == "the entity"
