# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from typer.testing import CliRunner

from RepoAuditor.EntryPoint import app


# ----------------------------------------------------------------------
def test_Version() -> None:
    result = CliRunner().invoke(app, ["Version"])

    assert result.exit_code == 0
    assert result.output
