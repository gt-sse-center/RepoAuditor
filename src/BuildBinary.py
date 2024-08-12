"""Builds the binary for this project."""

import datetime
import importlib
import re

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
    match = re.search(
        r"""(?#
        Copyright                           )Copyright(?#
        Mark [Optional]                     )(?P<mark>\s+\([cC]\))?(?#
        Year                                )\s+(?P<year>\d{4})(?#
        Year Range [Optional]               )(?:\s*-\s*\d{2,4})?(?#
        Suffix                              )(?P<suffix>.+)(?#
        End of line                         )$(?#
        )""",
        PathEx.EnsureFile(Path(__file__).parent.parent / "LICENSE.txt").read_text(),
        flags=re.MULTILINE,
    )

    current_year = datetime.datetime.now().year

    if not match:
        return f"Copyright {current_year} Scientific Software Engineering Center at Georgia Tech"

    initial_year = int(match.group("year"))

    if current_year == initial_year:
        year_suffix = ""
    elif current_year // 100 != initial_year // 100:
        year_suffix = f"-{current_year}"
    else:
        year_suffix = f"-{current_year % 100}"

    return f"Copyright{match.group('mark')} {initial_year}{year_suffix} Scientific Software Engineering Center at Georgia Tech"


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
