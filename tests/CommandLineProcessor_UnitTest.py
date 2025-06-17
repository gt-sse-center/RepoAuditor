# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit test for CommandLineProcessor.py"""

import re
import textwrap
from typing import Optional, cast
from unittest.mock import patch

import pytest
from dbrownell_Common.TestHelpers.StreamTestHelpers import GenerateDoneManagerAndContent
from dbrownell_Common.Types import override

from RepoAuditor.CommandLineProcessor import *
from RepoAuditor.Module import TypeDefinitionItemType
from RepoAuditor.Query import Query
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
class MyModule(Module):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str = "MyModule",
        dynamic_args: Optional[dict[str, Any]] = None,
        *,
        requires_explicit_include: bool = False,
    ):
        super().__init__(
            name,
            "",
            ExecutionStyle.Sequential,
            [MyQuery()],
            requires_explicit_include=requires_explicit_include,
        )

        self.dynamic_args = dynamic_args

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return self.dynamic_args or {}

    # ----------------------------------------------------------------------
    @override
    def GenerateInitialData(
        self,
        dynamic_args: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        assert not dynamic_args
        return dynamic_args


# ----------------------------------------------------------------------
class MyQuery(Query):
    # ----------------------------------------------------------------------
    def __init__(self):
        super().__init__(
            "MyQuery",
            ExecutionStyle.Sequential,
            [
                MyRequirement("Requirement1", requires_explicit_include=True, has_dynamic_args=False),
                MyRequirement("Requirement2", has_dynamic_args=True),
            ],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        return module_data


# ----------------------------------------------------------------------
class MyRequirement(Requirement):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        *,
        requires_explicit_include: bool = False,
        has_dynamic_args: bool = False,
    ):
        super().__init__(
            name,
            "",
            ExecutionStyle.Sequential,
            "",
            "",
            requires_explicit_include=requires_explicit_include,
        )

        self._has_dynamic_args = has_dynamic_args

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        if not self._has_dynamic_args:
            return {}

        return {"foo": int}

    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
    ) -> tuple[EvaluateResult, Optional[str]]:
        raise Exception("This should never be invoked")


# ----------------------------------------------------------------------
# |
# |  Public Functions
# |
# ----------------------------------------------------------------------
def test_Standard():
    clp = CommandLineProcessor.Create(
        lambda *args: {"MyModule-arg1": False},
        [MyModule()],
        [],
        [],
        set(),
        set(),
    )

    assert len(clp.module_infos) == 1
    assert isinstance(clp.module_infos[0].module, MyModule)
    assert clp.module_infos[0].module.GetNumRequirements() == 1
    assert clp.module_infos[0].dynamic_args == {"arg1": False}
    assert not clp.module_infos[0].requirement_args
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False

    dm_and_content = GenerateDoneManagerAndContent()

    with patch("RepoAuditor.CommandLineProcessor.Execute") as mock_execute:
        clp(next(dm_and_content))

    assert len(mock_execute.call_args_list) == 1

    args = mock_execute.call_args_list[0].args
    kwargs = mock_execute.call_args_list[0].kwargs

    assert len(args) == 2

    assert isinstance(args[0], DoneManager)
    assert args[1] == clp.module_infos

    assert kwargs == {}

    assert cast(str, next(dm_and_content)) == textwrap.dedent(
        """\
        Heading...DONE! (0, <scrubbed duration>)
        """,
    )


# ----------------------------------------------------------------------
def test_WithDynamicArgs():
    clp = CommandLineProcessor.Create(
        lambda *args: {
            "MyModule-arg1": False,
            "MyModule-one": 1,
            "MyModule-two": 2,
            "MyModule-Requirement2-foo": 123,
        },
        [MyModule(dynamic_args={"one": int, "two": int})],
        [],
        [],
        set(),
        set(),
    )

    assert len(clp.module_infos) == 1
    assert isinstance(clp.module_infos[0].module, MyModule)
    assert clp.module_infos[0].module.GetNumRequirements() == 1
    assert clp.module_infos[0].dynamic_args == {
        "arg1": False,
        "one": 1,
        "two": 2,
    }
    assert clp.module_infos[0].requirement_args == {
        "Requirement2": {"foo": 123},
    }
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
def test_IncludeModule():
    clp = CommandLineProcessor.Create(
        lambda *args: {},
        [MyModule(requires_explicit_include=True)],
        [],
        [],
        set(),
        set(),
    )

    assert not clp.module_infos
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False

    clp = CommandLineProcessor.Create(
        lambda *args: {},
        [MyModule(requires_explicit_include=True)],
        ["MyModule"],
        [],
        set(),
        set(),
    )

    assert len(clp.module_infos) == 1
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
def test_ExcludeModule():
    clp = CommandLineProcessor.Create(
        lambda *args: {},
        [MyModule()],
        [],
        ["MyModule"],
        set(),
        set(),
    )

    assert not clp.module_infos
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
@pytest.mark.parametrize("sep", ["-", "__--__"])
def test_IncludeRequirement(sep):
    clp = CommandLineProcessor.Create(
        lambda *args: {},
        [MyModule()],
        [f"MyModule{sep}Requirement1"],
        [],
        set(),
        set(),
        argument_separator=sep,
    )

    assert len(clp.module_infos) == 1
    assert clp.module_infos[0].module.GetNumRequirements() == 2
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
@pytest.mark.parametrize("sep", ["-", "__--__"])
def test_ExcludeRequirement(sep):
    clp = CommandLineProcessor.Create(
        lambda *args: {},
        [MyModule()],
        [],
        [f"MyModule{sep}Requirement2"],
        set(),
        set(),
        argument_separator=sep,
    )

    assert not clp.module_infos
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
def test_ExcludeAllRequirements():
    clp = CommandLineProcessor.Create(
        lambda *args: {},
        [MyModule()],
        [],
        ["MyModule-Requirement1", "MyModule-Requirement2"],
        set(),
        set(),
    )

    assert not clp.module_infos
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
@pytest.mark.parametrize("sep", ["-", "__--__"])
def test_CommandLineArgs(sep):
    clp = CommandLineProcessor.Create(
        lambda *args: {
            f"MyModule{sep}arg1": True,
        },
        [MyModule()],
        [],
        [],
        set(),
        set(),
        argument_separator=sep,
    )

    assert len(clp.module_infos) == 1
    assert clp.module_infos[0].module.GetNumRequirements() == 1
    assert clp.module_infos[0].dynamic_args == {"arg1": True}
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
def test_AllWarningsAsError():
    clp = CommandLineProcessor.Create(
        lambda *args: {"MyModule-arg1": False},
        [MyModule()],
        [],
        [],
        set(),
        set(),
        all_warnings_as_error=True,
    )

    assert len(clp.module_infos) == 1
    assert clp.warnings_as_error_module_names == {"MyModule"}
    assert clp.ignore_warnings_module_names == set()
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
def test_IgnoreAllWarnings():
    clp = CommandLineProcessor.Create(
        lambda *args: {"MyModule-arg1": False},
        [MyModule()],
        [],
        [],
        set(),
        set(),
        ignore_all_warnings=True,
    )

    assert len(clp.module_infos) == 1
    assert clp.warnings_as_error_module_names == set()
    assert clp.ignore_warnings_module_names == {"MyModule"}
    assert clp.single_threaded is False


# ----------------------------------------------------------------------
def test_ErrorInvalidModuleName():
    with pytest.raises(
        Exception,
        match=re.escape(
            "The module name 'Invalid-name' contains '-', which should be used as an argument separator."
        ),
    ):
        CommandLineProcessor.Create(
            lambda *args: {},
            [MyModule("Invalid-name")],
            [],
            [],
            set(),
            set(),
        )


# ----------------------------------------------------------------------
def test_ErrorDuplicateName():
    with pytest.raises(
        Exception,
        match=re.escape("The module 'MyModule' has already been defined."),
    ):
        CommandLineProcessor.Create(
            lambda *args: {},
            [MyModule(), MyModule()],
            [],
            [],
            set(),
            set(),
        )


# ----------------------------------------------------------------------
def test_ErrorInvalidIncludeName():
    with pytest.raises(
        Exception,
        match=re.escape("'DoesNotExist' is not a recognized module name."),
    ):
        CommandLineProcessor.Create(
            lambda *args: {"MyModule-arg1": False},
            [MyModule()],
            ["DoesNotExist"],
            [],
            set(),
            set(),
        )


# ----------------------------------------------------------------------
def test_ErrorInvalidExcludeName():
    with pytest.raises(
        Exception,
        match=re.escape("'DoesNotExist' is not a recognized module name."),
    ):
        CommandLineProcessor.Create(
            lambda *args: {"MyModule-arg1": False},
            [MyModule()],
            [],
            ["DoesNotExist"],
            set(),
            set(),
        )


# ----------------------------------------------------------------------
def test_InvalidArgName():
    with pytest.raises(
        Exception,
        match=re.escape("'MyModule' is not a recognized module name."),
    ):
        # This code provides an argument for a module that has been excluded
        CommandLineProcessor.Create(
            lambda *args: {"MyModule-arg1": False},
            [MyModule()],
            [],
            ["MyModule"],
            set(),
            set(),
        )


# ----------------------------------------------------------------------
def test_InvalidArgs():
    """Check if an invalid module is specified as an argument."""
    with pytest.raises(
        Exception,
        match=re.escape("'InvalidModule' is not a recognized module name."),
    ):
        CommandLineProcessor.Create(
            # Specify an unregistered module
            get_dynamic_args_func=lambda dynamic_arg_definitions: {"InvalidModule-arg1": "value"},
            # ValidModule is the registered module.
            modules=[MyModule(name="ValidModule")],
            includes=["InvalidModule"],
            excludes=[],
            warnings_as_error_module_names=set(),
            ignore_warnings_module_names=set(),
        )
