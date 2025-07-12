# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for GitHub/Impl/ClassicValueRequirementImpl.py"""

from pathlib import Path
from tempfile import TemporaryDirectory

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl
from RepoAuditor.Requirement import EvaluateResult


class MockDirectory:
    def __init__(self):
        self.name = "repository"


class TestExistsRequirementImpl:
    def test_Constructor(self):
        """Test the requirement implementation constructor."""
        requirement = ExistsRequirementImpl(
            name="Exists Some Value",
            filename="README.md",
            possible_locations=[
                "README.md",
            ],
            resolution="Get test to pass",
            rationale="For testing",
        )
        assert requirement.filename == "README.md"

    def test_Disabled(self):
        """Test disabled requirement."""
        requirement = ExistsRequirementImpl(
            name="Exists Some Value",
            filename="README.md",
            possible_locations=[
                "README.md",
            ],
            resolution="Get test to pass",
            rationale="For testing",
        )

        query_data = {}
        requirement_args = {"unrequired": True}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.DoesNotApply

    def test_NotFound(self):
        """Test for when file is not found."""
        requirement = ExistsRequirementImpl(
            name="Exists Some Value",
            filename="README.md",
            possible_locations=[
                "MEREAD.md",
            ],
            resolution="Get test to pass",
            rationale="For testing",
        )

        query_data = {"repo_dir": MockDirectory()}
        requirement_args = {"unrequired": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Error
        assert "No README.md file found" in result.context

    def test_Found(self):
        """Test for when file is found as is."""
        requirement = ExistsRequirementImpl(
            name="Exists Some Value",
            filename="README.md",
            possible_locations=[
                "README.md",
            ],
            resolution="Get test to pass",
            rationale="For testing",
        )

        tempdir = TemporaryDirectory()
        with open(Path(tempdir.name, "README.md"), "w") as f:
            f.write("temp file in temp directory")

        query_data = {"repo_dir": tempdir}
        requirement_args = {"unrequired": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
        assert "README.md found in repository" in result.context

    def test_FoundInDirectory(self):
        """Test if provided path is directory."""
        requirement = ExistsRequirementImpl(
            name="Exists Some Value",
            filename="README.md",
            possible_locations=[
                "docs",
            ],
            resolution="Get test to pass",
            rationale="For testing",
        )

        tempdir = TemporaryDirectory()
        # Create "docs" directory
        docs_dir = Path(tempdir.name) / "docs"
        docs_dir.mkdir(parents=True)

        with open(docs_dir / "README.md", "w") as f:
            f.write("temp file in temp directory")

        query_data = {"repo_dir": tempdir}
        requirement_args = {"unrequired": False}
        result = requirement.Evaluate(query_data, requirement_args)
        assert result.result == EvaluateResult.Success
        assert "File found in docs directory of the repository" in result.context
