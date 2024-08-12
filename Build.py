"""Build tasks for this python project."""

import sys

from pathlib import Path

import typer

from dbrownell_Common import PathEx
from dbrownell_DevTools.RepoBuildTools import Python as RepoBuildTools
from typer.core import TyperGroup


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
this_dir = PathEx.EnsureDir(Path(__file__).parent)
src_dir = PathEx.EnsureDir(this_dir / "src")
package_dir = PathEx.EnsureDir(src_dir / "RepoAuditor")


# ----------------------------------------------------------------------
Black = RepoBuildTools.BlackFuncFactory(this_dir, app)

Pylint = RepoBuildTools.PylintFuncFactory(
    package_dir,
    app,
    default_min_score=9.5,
)

Pytest = RepoBuildTools.PytestFuncFactory(
    this_dir,
    package_dir.name,
    app,
    default_min_coverage=90.0,
)

UpdateVersion = RepoBuildTools.UpdateVersionFuncFactory(
    src_dir,
    PathEx.EnsureFile(package_dir / "__init__.py"),
    app,
)

Package = RepoBuildTools.PackageFuncFactory(this_dir, app)
Publish = RepoBuildTools.PublishFuncFactory(this_dir, app)

BuildBinary = RepoBuildTools.BuildBinaryFuncFactory(
    this_dir,
    PathEx.EnsureFile(src_dir / "BuildBinary.py"),
    app,
)

CreateDockerImage = RepoBuildTools.CreateDockerImageFuncFactory(
    this_dir,
    app,
)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(app())
