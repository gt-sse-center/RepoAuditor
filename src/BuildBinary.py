# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Builds the binary for this project."""

import datetime
import importlib
import textwrap

from functools import cache
from pathlib import Path

from cx_Freeze import setup, Executable
from dbrownell_Common import PathEx


# ----------------------------------------------------------------------
@cache
def _GetName() -> str:
    return "RepoAuditor"


# ----------------------------------------------------------------------
@cache
def _GetVersionAndDocstring() -> tuple[str, str]:
    mod = importlib.import_module(_GetName())
    return mod.__version__, mod.__doc__ or ""


# ----------------------------------------------------------------------
@cache
def _GetEntryPoint() -> Path:
    return PathEx.EnsureFile(Path(__file__).parent / _GetName() / "EntryPoint.py")


# ----------------------------------------------------------------------
@cache
def _GetCopyright() -> str:
    initial_year = 2024
    current_year = datetime.datetime.now().year

    if current_year == initial_year:
        year_suffix = ""
    elif current_year // 100 != initial_year // 100:
        year_suffix = str(current_year)
    else:
        year_suffix = "-{}".format(current_year % 100)

    return textwrap.dedent(
        f"""\
        Copyright (c) {initial_year}{year_suffix} Scientific Software Engineering Center at Georgia Tech

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """,
    )


# ----------------------------------------------------------------------
setup(
    name=_GetName(),
    version=_GetVersionAndDocstring()[0],
    description=_GetVersionAndDocstring()[1],
    executables=[
        Executable(
            _GetEntryPoint(),
            base="console",
            copyright=_GetCopyright(),
            # icon=<icon_filename>,
            target_name=_GetName(),
            # trademarks=<trademarks>,
        ),
    ],
    options={
        "build_exe": {
            "excludes": [
                "tcl",
                "tkinter",
            ],
            "no_compress": False,
            "optimize": 0,
            # "packages": [],
            # "include_files": [],
        },
    },
)
