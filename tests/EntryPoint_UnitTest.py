# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

import pytest
import typer

from dbrownell_Common.TestHelpers.StreamTestHelpers import InitializeStreamCapabilities
from dbrownell_Common.TyperEx import TypeDefinitionItem  # type: ignore [import-untyped]
from typer.testing import CliRunner

from RepoAuditor import __version__
from RepoAuditor.EntryPoint import app, TypeInfoToString

from .Plugins.utilities import GetGithubUrl


# ----------------------------------------------------------------------
@pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)
# ----------------------------------------------------------------------
def test_Version() -> None:
    result = CliRunner().invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.output == f"RepoAuditor v{__version__}\n"


# ----------------------------------------------------------------------
def test_Standard() -> None:
    result = CliRunner().invoke(app, [])

    assert result.exit_code == 1
    assert "There are no modules to process." in result.output


# ----------------------------------------------------------------------
@pytest.mark.skip(reason="This test isn't stable due to GitHub rate limiting for requests without a PAT.")
def test_GitHub() -> None:
    result = CliRunner().invoke(
        app,
        [
            "--include",
            "GitHub",
            "--GitHub-url",
            GetGithubUrl(),
        ],
    )

    assert result.exit_code == 1, result.output
    assert "Incomplete data was encountered; please provide the GitHub PAT." in result.output


# ----------------------------------------------------------------------
def test_Help() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Module Information" in result.output


def test_TypeInfoToString() -> None:
    """Test the TypeInfoToString function to ensure valid command line output."""
    result = TypeInfoToString(
        "test_arg",
        (
            bool,
            typer.Option(
                False,
                help="Help text.",
            ),
        ),
    )
    expected_string = "    test_arg                                           bool    Help text."
    assert expected_string == result

    result = TypeInfoToString(
        "test_arg",
        TypeDefinitionItem(
            bool,
            typer.models.ParameterInfo(
                default=False,
                help="TypeDefinitionItem",
            ),
        ),
    )
    expected_string = "    test_arg                                           bool    TypeDefinitionItem"
    assert expected_string == result

    result = TypeInfoToString(
        "test_none",
        bool,
    )
    expected_string = "    test_none                                          bool    "
    assert expected_string == result
