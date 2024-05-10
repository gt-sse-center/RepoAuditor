# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the CommandLineProcessor object"""

from dataclasses import dataclass, field
from typing import Any, Protocol

from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]

from .ExecuteModules import Execute, Module, ModuleInfo


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class CommandLineProcessor:
    """\
    Object that makes it easy to process command line arguments and invoke ExecuteModules.Execute
    in a testable way.
    """

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class GetDynamicArgsFunc(Protocol):
        def __call__(
            self,
            dynamic_arg_definitions: dict[
                str, Any
            ],  # actual type is dict[str, TyperEx.TypeDefinitionItemType]
        ) -> dict[str, Any]: ...

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
        excludes: list[str],
        warnings_as_error_module_names: set[str],
        ignore_warnings_module_names: set[str],
        *,
        all_warnings_as_error: bool = False,
        ignore_all_warnings: bool = False,
        single_threaded: bool = False,
        argument_separator: str = "-",
    ) -> "CommandLineProcessor":
        # Convert modules into a lookup map
        module_map: dict[str, Module] = {}

        for module in modules:
            if argument_separator in module.name:
                raise Exception(f"The module name '{module.name}' contains '{argument_separator}'.")

            prev_module = module_map.get(module.name, None)
            if prev_module is not None:
                raise Exception(f"The module '{module.name}' has already been defined.")

            module_map[module.name] = module

        del modules

        # Process excludes
        excluded_requirements: dict[str, set[str]] = {}

        for exclude in excludes:
            parts = exclude.split(argument_separator)

            this_module = module_map.get(parts[0], None)
            if this_module is None:
                raise Exception(f"'{parts[0]}' is not a recognized module name.")

            if len(parts) == 1:
                module_map.pop(parts[0])
            else:
                excluded_requirements.setdefault(this_module.name, set()).add(
                    argument_separator.join(parts[1:])
                )

        del excludes

        for module_name, excluded_requirement_names in excluded_requirements.items():
            module = module_map[module_name]
            module.RemoveRequirements(excluded_requirement_names)

        del excluded_requirements

        for module_name, module in list(module_map.items()):
            if module.GetNumRequirements() == 0:
                module_map.pop(module_name)

        if all_warnings_as_error:
            warnings_as_error_module_names = {module.name for module in module_map.values()}
        if ignore_all_warnings:
            ignore_warnings_module_names = {module.name for module in module_map.values()}

        # Create the type definitions
        dynamic_arg_definitions: dict[str, Any] = {}

        for module in module_map.values():
            for key, value in module.GetDynamicArgDefinitions().items():
                dynamic_arg_definitions[f"{module.name}{argument_separator}{key}"] = value

        # Process the dynamic info
        dynamic_args: dict[str, dict[str, Any]] = {}

        for key, value in get_dynamic_args_func(dynamic_arg_definitions).items():
            parts = key.split(argument_separator)
            assert len(parts) >= 2

            if parts[0] not in module_map:
                raise Exception(f"'{parts[0]}' is not a recognized module name.")

            dynamic_args.setdefault(parts[0], {})[argument_separator.join(parts[1:])] = value

        return cls(
            [
                ModuleInfo(module, dynamic_args.get(module_name, {}))
                for module_name, module in module_map.items()
            ],
            warnings_as_error_module_names,
            ignore_warnings_module_names,
            single_threaded=single_threaded,
        )

    # ----------------------------------------------------------------------
    def __call__(
        self,
        dm: DoneManager,
    ) -> None:
        Execute(dm, self.module_infos)
