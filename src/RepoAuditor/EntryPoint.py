# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""This file serves as an example of how to create scripts that can be invoked from the command line once the package is installed."""

import sys
import textwrap

from typing import Annotated

import pluggy
import typer

from click.exceptions import UsageError
from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags  # type: ignore [import-untyped]
from dbrownell_Common import TextwrapEx  # type: ignore [import-untyped]
from dbrownell_Common import TyperEx  # type: ignore [import-untyped]
from typer.core import TyperGroup  # type: ignore [import-untyped]

from RepoAuditor import APP_NAME, __version__
from RepoAuditor.CommandLineProcessor import CommandLineProcessor, Module
from RepoAuditor import Plugin


# ----------------------------------------------------------------------
ARGUMENT_SEPARATOR = "-"


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
def _GetModules() -> list[Module]:
    plugin_manager = pluggy.PluginManager(APP_NAME)

    plugin_manager.add_hookspecs(Plugin)
    plugin_manager.load_setuptools_entrypoints(APP_NAME)

    return plugin_manager.hook.GetModule()


_all_modules = _GetModules()
del _GetModules


# ----------------------------------------------------------------------
def _HelpEpilog() -> str:
    content: list[str] = []

    for module in _all_modules:
        arguments: list[str] = []

        for arg_name, type_info in module.GetDynamicArgDefinitions().items():
            if isinstance(type_info, TyperEx.TypeDefinitionItem):
                python_type = type_info.python_type
                parameter_info = type_info.parameter_info
            elif isinstance(type_info, tuple):
                python_type = type_info[0]
                parameter_info = type_info[1]
            else:
                python_type = type_info
                parameter_info = None

            arguments.append(
                "    {arg_name:<32} {type_description:<8} {help}".format(
                    arg_name=f"--{module.name}{ARGUMENT_SEPARATOR}{arg_name}",
                    type_description=python_type.__name__,
                    help="" if parameter_info is None else parameter_info.help,
                ),
            )

        final_arguments = TextwrapEx.Indent(
            "\n".join(arguments),
            4,
            skip_first_line=True,
        )

        content.append(
            textwrap.dedent(
                f"""\
                {module.name}
                {"-" * len(module.name)}
                {module.description}

                Command Line Arguments:
                    {final_arguments}
                """,
            ),
        )

    return (
        textwrap.dedent(
            """\
        Module Information
        ==================

        {}
        """,
        )
        .format(
            "\n".join(content),
        )
        .replace("\n", "\n\n")
    )


# ----------------------------------------------------------------------
def _VersionCallback(value: bool) -> None:
    if value:
        sys.stdout.write(f"RepoAuditor v{__version__}\n")
        raise typer.Exit()


# ----------------------------------------------------------------------
@app.command(
    "EntryPoint",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=__doc__,
    epilog=_HelpEpilog(),
    no_args_is_help=False,
)
def EntryPoint(
    ctx: typer.Context,
    version: Annotated[  # pylint: disable=unused-argument
        bool,
        typer.Option(
            "--version",
            help="Display the version of this tool and exit.",
            callback=_VersionCallback,
            is_eager=True,
        ),
    ] = False,
    excludes: Annotated[
        list[str],
        typer.Option(
            "--exclude",
            help=f"Module or requirement names to exclude from execution; like other command line arguments, requirement names must include the module name as a prefix (e.g. 'ModuleName{ARGUMENT_SEPARATOR}RequirementName'). This value can be provided multiple times.",
        ),
    ] = [],
    warnings_as_error: Annotated[
        list[str],
        typer.Option(
            "--warnings-as-error",
            help="Name of a module whose warnings should be treated as errors. This value can be provided multiple times.",
        ),
    ] = [],
    ignore_warnings: Annotated[
        list[str],
        typer.Option(
            "--ignore-warnings",
            help="Name of a module whose warnings should be ignored. This value can be provided multiple times.",
        ),
    ] = [],
    all_warnings_as_error: Annotated[
        bool, typer.Option("--all-warnings-as-error", help="Treat all warnings as errors.")
    ] = False,
    ignore_all_warnings: Annotated[
        bool, typer.Option("--ignore-all-warnings", help="Ignore all warnings.")
    ] = False,
    single_threaded: Annotated[
        bool,
        typer.Option(
            "--single-threaded", help="Do not use multiple threads when evaluating requirements."
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            help="Write verbose information to the terminal.",
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Write debug information to the terminal.",
        ),
    ] = False,
) -> None:
    with DoneManager.CreateCommandLine(
        sys.stdout,
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        try:
            executor = CommandLineProcessor.Create(
                lambda dynamic_arg_definitions: TyperEx.ProcessDynamicArgs(
                    ctx, dynamic_arg_definitions
                ),
                _all_modules,
                excludes,
                set(warnings_as_error),
                set(ignore_warnings),
                all_warnings_as_error=all_warnings_as_error,
                ignore_all_warnings=ignore_all_warnings,
                single_threaded=single_threaded,
                argument_separator=ARGUMENT_SEPARATOR,
            )

        except Exception as ex:
            if dm.is_debug:
                raise

            raise UsageError(str(ex)) from ex

        dm.WriteLine("")

        executor(dm)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
