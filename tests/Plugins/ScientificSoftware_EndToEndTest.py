# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""End-to-end tests for the ScientificSoftware plugin."""

import pytest
from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    InitializeStreamCapabilities,
)
from typer.testing import CliRunner
from utilities import ScrubDurationGithuburlAndSpaces

from RepoAuditor.EntryPoint import app

# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


# ----------------------------------------------------------------------
class TestScientificSoftware:
    """End-to-end tests for files in a GitHub repository which implements scientific software."""

    # ----------------------------------------------------------------------
    def test_NoCitation(self, args, snapshot):
        """Test if no CITATION file exists in the repository."""
        result = CliRunner().invoke(
            app,
            args,
        )

        assert result.exit_code == -1, result.output
        assert ScrubDurationGithuburlAndSpaces(result.stdout) == snapshot
