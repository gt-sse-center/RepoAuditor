# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the Plugin2 object"""

from typing import Any

import pluggy

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor import APP_NAME
from RepoAuditor.Plugin import Module
from RepoAuditor.Query import ExecutionStyle


# ----------------------------------------------------------------------
class Plugin2(Module):
    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super(Plugin2, self).__init__(
            "Plugin2",
            "This is a description of Plugin2",
            ExecutionStyle.Parallel,
            [],
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
        assert "foo" in dynamic_args
        return dynamic_args


# ----------------------------------------------------------------------
@pluggy.HookimplMarker(APP_NAME)
def GetModule() -> Module:
    return Plugin2()
