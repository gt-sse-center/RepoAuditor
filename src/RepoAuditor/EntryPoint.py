# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""This file serves as an example of how to create scripts that can be invoked from the command line once the package is installed."""

import sys

import typer

from typer.core import TyperGroup  # type: ignore [import-untyped]

from RepoAuditor import Math, __version__


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
@app.command("Add")
def Add(
    x: int,
    y: int,
) -> None:
    """Adds 2 values."""

    sys.stdout.write(str(Math.Add(x, y)))


# ----------------------------------------------------------------------
@app.command("Sub")
def Sub(
    x: int,
    y: int,
) -> None:
    """Subtracts 2 values."""

    sys.stdout.write(str(Math.Sub(x, y)))


# ----------------------------------------------------------------------
@app.command("Mult")
def Mult(
    x: int,
    y: int,
) -> None:
    """Multiplies 2 values."""

    sys.stdout.write(str(Math.Mult(x, y)))


# ----------------------------------------------------------------------
@app.command("Div")
def Div(
    x: int,
    y: int,
) -> None:
    """Divides 1 value by another."""

    sys.stdout.write(str(Math.Div(x, y)))


# ----------------------------------------------------------------------
@app.command("Version")
def Version() -> None:
    """Prints the version of the package."""

    sys.stdout.write(__version__)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
