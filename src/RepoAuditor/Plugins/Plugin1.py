# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the Plugin1 object"""

from typing import Any, Optional

import pluggy

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor import APP_NAME
from RepoAuditor.Plugin import Module
from RepoAuditor.Query import ExecutionStyle, Query
from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
class Plugin1(Module):
    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super(Plugin1, self).__init__(
            "Plugin1",
            "This is a description of Plugin1",
            ExecutionStyle.Parallel,
            [_Query()],
        )

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            "foo": int,
        }

    # ----------------------------------------------------------------------
    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> dict[str, Any]:
        if "foo" not in dynamic_args:
            raise Exception("'foo' is a required argument.")

        return dynamic_args


# ----------------------------------------------------------------------
@pluggy.HookimplMarker(APP_NAME)
def GetModule() -> Module:
    return Plugin1()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class _Requirement(Requirement):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(_Requirement, self).__init__(
            "Requirement1",
            "A description of the requirement.",
            ExecutionStyle.Sequential,
            "resolution_template",
            "rationale_template",
        )

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
    ) -> tuple[EvaluateResult, Optional[str]]:
        return EvaluateResult.Success, None


# ----------------------------------------------------------------------
class _Query(Query):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(_Query, self).__init__(
            "Query1",
            ExecutionStyle.Sequential,
            [_Requirement()],
        )

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        return module_data
