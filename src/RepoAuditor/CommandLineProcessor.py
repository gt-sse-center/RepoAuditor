# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the CommandLineProcessor object."""

from dataclasses import dataclass, field
from typing import Any, Protocol

from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]

from RepoAuditor.ExecuteModules import Execute, Module, ModuleInfo


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class CommandLineProcessor:
    """Class for processing command line arguments and invoking the appropriate modules.

    Object that makes it easy to process command line arguments and invoke ExecuteModules.Execute
    in a testable way.
    """

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class GetDynamicArgsFunc(Protocol):
        def __call__(  # noqa: D102
            self,
            dynamic_arg_definitions: dict[
                str, Any
            ],  # actual type is dict[str, TyperEx.TypeDefinitionItemType]
        ) -> dict[str, Any]: ...

    @staticmethod
    def _GetModuleMap(
        modules: list[Module],
        argument_separator: str,
    ) -> dict[str, Module]:
        """Convert modules into a lookup map.

        Returns a dict of module names mapped to the corresponding module.
        """
        module_map: dict[str, Module] = {}

        for module in modules:
            if argument_separator in module.name:
                msg = f"The module name '{module.name}' contains '{argument_separator}', which should be used as an argument separator."
                raise ValueError(msg)

            prev_added_module = module_map.get(module.name, None)
            if prev_added_module is not None:
                msg = f"The module '{module.name}' has already been defined."
                raise ValueError(msg)

            module_map[module.name] = module

        return module_map

    @staticmethod
    def _ProcessIncludes(
        module_map: dict[str, Module],
        includes: list[str],
        argument_separator: str,
    ) -> tuple[set[str], dict[str, set[str]]]:
        """Process the modules and requirements to include.

        Returns both the set of names of the included modules as well as
        the dictionary of module names mapped to the set of included requirement names.
        """
        included_modules: set[str] = set()
        included_requirements: dict[str, set[str]] = {}

        for include in includes:
            parts = include.split(argument_separator)

            this_module = module_map.get(parts[0], None)
            if this_module is None:
                msg = f"'{parts[0]}' is not a recognized module name."
                raise ValueError(msg)

            if len(parts) == 1:
                included_modules.add(parts[0])
            else:
                included_requirements.setdefault(this_module.name, set()).add(
                    argument_separator.join(parts[1:])
                )

        return included_modules, included_requirements

    @staticmethod
    def _ProcessExcludes(
        module_map: dict[str, Module],
        excludes: list[str],
        argument_separator: str,
    ) -> dict[str, set[str]]:
        """Process the modules and requirements to exclude.

        Returns both the set of names of the excluded modules as well as
        the dictionary of module names mapped to the set of excluded requirement names.
        """
        excluded_requirements: dict[str, set[str]] = {}

        for exclude in excludes:
            parts = exclude.split(argument_separator)

            this_module = module_map.get(parts[0], None)
            if this_module is None:
                msg = f"'{parts[0]}' is not a recognized module name."
                raise ValueError(msg)

            if len(parts) == 1:
                module_map.pop(parts[0])
            else:
                excluded_requirements.setdefault(this_module.name, set()).add(
                    argument_separator.join(parts[1:])
                )

        return excluded_requirements

    @staticmethod
    def _ProcessDynamicArguments(
        module_map: dict[str, Module],
        argument_separator: str,
        get_dynamic_args_func: "CommandLineProcessor.GetDynamicArgsFunc",
    ) -> dict[str, dict[str, Any]]:
        """Process the passed in dynamic arguments.

        Returns a dictionary of module names to a corresponding dictionary
        of argument names to values.
        """
        # First we create the type definitions
        dynamic_arg_definitions: dict[str, Any] = {}

        for module in module_map.values():
            # Module-level args
            for key, value in module.GetDynamicArgDefinitions().items():
                dynamic_arg_definitions[f"{module.name}{argument_separator}{key}"] = value

            # Requirement-level args
            for query in module.queries:
                for requirement in query.requirements:
                    for key, value in requirement.GetDynamicArgDefinitions().items():
                        dynamic_arg_definitions[
                            f"{module.name}{argument_separator}{requirement.name}{argument_separator}{key}"
                        ] = value

        # Now we process the definitions to get the dynamic arguments
        dynamic_args: dict[str, dict[str, Any]] = {}

        num_acceptable_dynamic_args_parts = 2

        for key, value in get_dynamic_args_func(dynamic_arg_definitions).items():
            parts = key.split(argument_separator)
            assert len(parts) >= num_acceptable_dynamic_args_parts

            if parts[0] not in module_map:
                msg = f"'{parts[0]}' is not a recognized module name."
                raise ValueError(msg)

            if len(parts) == num_acceptable_dynamic_args_parts:
                dynamic_args.setdefault(parts[0], {})[parts[1]] = value
            else:
                dynamic_args.setdefault(parts[0], {}).setdefault(None, {}).setdefault(  # type: ignore[call-overload]
                    parts[1],
                    {},
                )[argument_separator.join(parts[2:])] = value

        return dynamic_args

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    module_infos: list[ModuleInfo]
    warnings_as_error_module_names: set[str]
    ignore_warnings_module_names: set[str]
    single_threaded: bool = field(kw_only=True)

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    @classmethod
    def Create(
        cls,
        get_dynamic_args_func: "CommandLineProcessor.GetDynamicArgsFunc",
        modules: list[Module],
        includes: list[str],
        excludes: list[str],
        warnings_as_error_module_names: set[str],
        ignore_warnings_module_names: set[str],
        *,
        all_warnings_as_error: bool = False,
        ignore_all_warnings: bool = False,
        single_threaded: bool = False,
        argument_separator: str = "-",
    ) -> "CommandLineProcessor":
        """Factor method to construct a CommandLineProcessor object."""
        # Convert modules into a lookup map
        module_map: dict[str, Module] = cls._GetModuleMap(modules, argument_separator)

        del modules

        # Process includes
        included_modules, included_requirements = cls._ProcessIncludes(
            module_map, includes, argument_separator
        )

        del includes

        for module_name, module in list(module_map.items()):
            if module.requires_explicit_include and module_name not in included_modules:
                module_map.pop(module_name)
                continue

        del included_modules

        # Process excludes
        excluded_requirements: dict[str, set[str]] = cls._ProcessExcludes(
            module_map, excludes, argument_separator
        )

        del excludes

        # Add / Remove the requirements for each module
        for module_name, module in list(module_map.items()):
            module.ProcessRequirements(
                included_requirements.get(module_name, set()),
                excluded_requirements.get(module_name, set()),
            )

            if module.GetNumRequirements() == 0:
                module_map.pop(module_name)

        del included_requirements
        del excluded_requirements

        if all_warnings_as_error:
            warnings_as_error_module_names = {module.name for module in module_map.values()}
        if ignore_all_warnings:
            ignore_warnings_module_names = {module.name for module in module_map.values()}

        # Process the dynamic info
        dynamic_args: dict[str, dict[str, Any]] = cls._ProcessDynamicArguments(
            module_map, argument_separator, get_dynamic_args_func
        )

        module_infos: list[ModuleInfo] = []

        for module_name, module in module_map.items():
            module_args = dynamic_args.get(module_name, {})
            requirement_args = module_args.pop(None, None)  # type: ignore[call-overload]

            module_infos.append(ModuleInfo(module, module_args, requirement_args))

        return cls(
            module_infos,
            warnings_as_error_module_names,
            ignore_warnings_module_names,
            single_threaded=single_threaded,
        )

    # ----------------------------------------------------------------------
    def __call__(  # noqa: D102
        self,
        dm: DoneManager,
    ) -> list[list[Module.EvaluateInfo]]:
        return Execute(dm, self.module_infos)
