# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from typer.testing import CliRunner

from RepoAuditor import __version__
from RepoAuditor.EntryPoint import app


# ----------------------------------------------------------------------
def test_Add():
    result = CliRunner().invoke(app, ["Add", "1", "20"])
    assert result.exit_code == 0
    assert result.stdout == "21"


# ----------------------------------------------------------------------
def test_Sub():
    result = CliRunner().invoke(app, ["Sub", "1", "20"])
    assert result.exit_code == 0
    assert result.stdout == "-19"


# ----------------------------------------------------------------------
def test_Mult():
    result = CliRunner().invoke(app, ["Mult", "2", "15"])
    assert result.exit_code == 0
    assert result.stdout == "30"


# ----------------------------------------------------------------------
def test_Div():
    result = CliRunner().invoke(app, ["Div", "6", "3"])
    assert result.exit_code == 0
    assert result.stdout == "2.0"


# ----------------------------------------------------------------------
def test_Version():
    result = CliRunner().invoke(app, ["Version"])
    assert result.exit_code == 0
    assert result.stdout == __version__


# ----------------------------------------------------------------------
def test_NoArgs():
    result = CliRunner().invoke(app, [])
    assert result.exit_code == 0
    assert "Add" in result.stdout
    assert "Sub" in result.stdout
    assert "Mult" in result.stdout
    assert "Div" in result.stdout
    assert "Version" in result.stdout
