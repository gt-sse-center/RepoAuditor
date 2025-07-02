# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Common test fixtures for full test suite"""

import os
import sys

import pytest


@pytest.fixture(autouse=True)
def fixed_terminal_size(monkeypatch):
    """Automatically set terminal to a fixed size for snapshot testing.
    This way the user's terminal size won't matter, leading to consistency.
    """
    monkeypatch.setattr(
        os,
        "get_terminal_size",
        lambda fd=sys.stdout.fileno(): os.terminal_size((120, 100)),
    )
