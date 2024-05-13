# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from typer.testing import CliRunner

from RepoAuditor import __version__
from RepoAuditor.EntryPoint import app


# ----------------------------------------------------------------------
def test_Version() -> None:
    result = CliRunner().invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.output == f"RepoAuditor v{__version__}\n"


# ----------------------------------------------------------------------
def test_Standard() -> None:
    result = CliRunner().invoke(app, ["--Plugin1-foo", "10"])

    assert result.exit_code == 0
    assert result.output


# ----------------------------------------------------------------------
def test_Exception() -> None:
    result = CliRunner().invoke(app, [])

    assert result.exit_code != 0

    # Don't assert as a single string as the "ERROR:" prefix is decorated with colors
    assert "ERROR:" in result.output
    assert "'foo' is a required argument." in result.output


# ----------------------------------------------------------------------
def test_ExceptionWithDebug() -> None:
    result = CliRunner().invoke(app, ["--debug"])

    assert result.exit_code != 0
    assert "Exception: 'foo' is a required argument" in result.output


# ----------------------------------------------------------------------
def test_Help() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Module Information" in result.output
