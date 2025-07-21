# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Audits a repository against a set of requirements."""

import os
import sys
import textwrap
import traceback
from typing import Annotated, Optional

import pluggy
import typer
from click.exceptions import UsageError
from dbrownell_Common import (
    TextwrapEx,  # type: ignore [import-untyped]
    TyperEx,  # type: ignore [import-untyped]
)
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Streams.DoneManager import Flags as DoneManagerFlags  # type: ignore [import-untyped]
from typer.core import TyperGroup  # type: ignore [import-untyped]
from typer_config.decorators import use_yaml_config

from RepoAuditor import APP_NAME, Plugin, __version__
from RepoAuditor.CommandLineProcessor import CommandLineProcessor, Module
from RepoAuditor.Display import DisplayResults

# ----------------------------------------------------------------------
ARGUMENT_SEPARATOR = "-"


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    """Group commands in natural order."""

    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs) -> list[str]:  # noqa: ARG002  # pragma: no cover
        """Return a list of all the commands, to be sorted in a natural ordering."""
        return list(self.commands.keys())


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
def TypeInfoToString(
    arg_name: str,
    type_info: TyperEx.TypeDefinitionItemType,
) -> str:
    """Convert type information from command line arguments to a string representation.

    Args:
        arg_name (str): The name of the command line argument.
        type_info (TyperEx.TypeDefinitionItemType): Type information for the accepted value.

    Returns:
        str: String description of the command line argument.

    """
    if isinstance(type_info, TyperEx.TypeDefinitionItem):
        python_type = type_info.python_type
        parameter_info = type_info.parameter_info
    elif isinstance(type_info, tuple):
        python_type = type_info[0]
        parameter_info = type_info[1]
    else:
        python_type = type_info
        parameter_info = None

    return "    {arg_name:<50} {type_description:<7} {help}".format(
        arg_name=arg_name,
        type_description=python_type.__name__,
        help="" if parameter_info is None else parameter_info.help,
    )


# ----------------------------------------------------------------------
def _HelpEpilog() -> str:
    content: list[str] = []

    # ----------------------------------------------------------------------

    for module in _all_modules:
        # Get the module arguments
        module_arguments: list[str] = []

        for arg_name, type_info in module.GetDynamicArgDefinitions().items():
            module_arguments.append(
                TypeInfoToString(
                    f"--{module.name}{ARGUMENT_SEPARATOR}{arg_name}",
                    type_info,
                )
            )

        final_module_arguments = TextwrapEx.Indent(
            "\n".join(module_arguments),
            4,
            skip_first_line=True,
        )

        # Get the requirement arguments
        requirement_arguments: list[str] = []

        for query in module.queries:
            for requirement in query.requirements:
                for key, value in requirement.GetDynamicArgDefinitions().items():
                    requirement_arguments.append(
                        TypeInfoToString(
                            f"--{module.name}{ARGUMENT_SEPARATOR}{requirement.name}{ARGUMENT_SEPARATOR}{key}",
                            value,
                        ),
                    )

        final_requirement_arguments = TextwrapEx.Indent(
            "\n".join(requirement_arguments),
            4,
            skip_first_line=True,
        )

        content.append(
            textwrap.dedent(
                f"""\
                {"-" * len(module.name)}
                {module.name}
                {"-" * len(module.name)}
                {module.description}

                Command Line Arguments:
                    {final_module_arguments}

                Optional Arguments:
                    {final_requirement_arguments}
                """,
            ),
        )

    return (
        textwrap.dedent(
            """\
        Module Information
        ==================

        {}

        Command Line Examples
        =====================
        repo_auditor --include GitHub --GitHub-url https://github.com/gt-sse-center/RepoAuditor --GitHub-pat <PAT or path to file containing PAT>

        """,
        )
        .format(
            "\n".join(content),
        )
        .replace("\n", "\n\n")
    )


# ----------------------------------------------------------------------
def _VersionCallback(value: bool) -> None:  # noqa: FBT001
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
@use_yaml_config()
def EntryPoint(  # noqa: PLR0913  # pragma: no cover
    ctx: typer.Context,
    version: Annotated[  # noqa: ARG001, FBT002
        bool,
        typer.Option(
            "--version",
            help="Display the version of this tool and exit.",
            callback=_VersionCallback,
            is_eager=True,
        ),
    ] = False,
    includes: Annotated[
        Optional[list[str]],
        typer.Option(
            "--include",
            help=f"Module or requirement names to explicitly include in the execution; like other command line arguments, requirement names must include the module name as a prefix (e.g. 'ModuleName{ARGUMENT_SEPARATOR}RequirementName'). This value can be provided multiple times.",
        ),
    ] = None,
    excludes: Annotated[
        Optional[list[str]],
        typer.Option(
            "--exclude",
            help=f"Module or requirement names to exclude from execution; like other command line arguments, requirement names must include the module name as a prefix (e.g. 'ModuleName{ARGUMENT_SEPARATOR}RequirementName'). This value can be provided multiple times.",
        ),
    ] = None,
    warnings_as_error: Annotated[
        Optional[list[str]],
        typer.Option(
            "--warnings-as-error",
            help="Name of a module whose warnings should be treated as errors. This value can be provided multiple times.",
        ),
    ] = None,
    ignore_warnings: Annotated[
        Optional[list[str]],
        typer.Option(
            "--ignore-warnings",
            help="Name of a module whose warnings should be ignored. This value can be provided multiple times.",
        ),
    ] = None,
    all_warnings_as_error: Annotated[  # noqa: FBT002
        bool, typer.Option("--all-warnings-as-error", help="Treat all warnings as errors.")
    ] = False,
    ignore_all_warnings: Annotated[  # noqa: FBT002
        bool, typer.Option("--ignore-all-warnings", help="Ignore all warnings.")
    ] = False,
    single_threaded: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--single-threaded", help="Do not use multiple threads when evaluating requirements."),
    ] = False,
    no_resolution: Annotated[  # noqa: FBT002
        bool,
        typer.Option(
            "--no-resolution",
            help="Do not display resolution information for requirements that are not successful.",
        ),
    ] = False,
    no_rationale: Annotated[  # noqa: FBT002
        bool,
        typer.Option(
            "--no-rationale",
            help="Do not display rationale information for requirements that are not successful.",
        ),
    ] = False,
    verbose: Annotated[  # noqa: FBT002
        bool,
        typer.Option(
            "--verbose",
            help="Write verbose information to the terminal.",
        ),
    ] = False,
    debug: Annotated[  # noqa: FBT002
        bool,
        typer.Option(
            "--debug",
            help="Write debug information to the terminal.",
        ),
    ] = False,
) -> None:
    """Entry point for the command line interface."""
    # Initialize lists to avoid mutable default arguments
    includes = includes or []
    excludes = excludes or []
    warnings_as_error = warnings_as_error or []
    ignore_warnings = ignore_warnings or []

    with DoneManager.CreateCommandLine(
        sys.stdout,
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        try:
            executor = CommandLineProcessor.Create(
                lambda dynamic_arg_definitions: TyperEx.ProcessDynamicArgs(ctx, dynamic_arg_definitions),
                _all_modules,
                includes,
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

        try:
            all_results = executor(dm)

            dm.WriteLine("\n\n")

            # Try to set panel width
            try:
                panel_width = min(
                    os.get_terminal_size().columns,
                    dm.capabilities.DEFAULT_COLUMNS,
                )
            except OSError:
                # Exception if not connected to a terminal
                # in which case default to None
                panel_width = None

            DisplayResults(
                dm,
                all_results,
                display_resolution=not no_resolution,
                display_rationale=not no_rationale,
                panel_width=panel_width,
            )
        except Exception as ex:
            error = traceback.format_exc() if dm.is_debug else str(ex)
            dm.WriteError(error)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
