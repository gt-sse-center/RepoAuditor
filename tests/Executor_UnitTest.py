# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Unit test for Executor.py"""

import sys
import time

from dataclasses import dataclass

import pytest

from dbrownell_Common.Types import override

from RepoAuditor.Executor import *
from RepoAuditor.Module import *
from RepoAuditor.Requirement import *


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyModule(Module):
    @override
    def _GetData(self) -> Optional[dict[str, Any]]:
        return {"module_name": self.name}


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyQuery(Query):
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        module_data["query_name"] = self.name
        return module_data


# ----------------------------------------------------------------------
class MyRequirement(Requirement):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        description: str,
        style: ExecutionStyle,
        resolution_template: str,
        rationale_template: str,
        result: EvaluateResult,
    ) -> None:
        super(MyRequirement, self).__init__(
            name, description, style, resolution_template, rationale_template
        )
        self.result = result

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
    ) -> tuple[EvaluateResult, Optional[str]]:
        # Introduce a delay so that we can see things happening
        time.sleep(0.1)

        return self.result, None


# ----------------------------------------------------------------------
@pytest.mark.parametrize("single_threaded", [False, True])
def test_Successful(single_threaded):
    modules: list[Module] = []

    # ----------------------------------------------------------------------
    def GetExecutionStyle(index: int) -> ExecutionStyle:
        return ExecutionStyle.Parallel if index % 2 == 0 else ExecutionStyle.Sequential

    # ----------------------------------------------------------------------

    for module_index in range(5):
        queries: list[Query] = []

        for query_index in range(4):
            requirements: list[Requirement] = []

            for requirement_index in range(5):
                requirements.append(
                    MyRequirement(
                        f"Requirement-{module_index}-{query_index}-{requirement_index}",
                        "",
                        GetExecutionStyle(requirement_index),
                        "",
                        "",
                        EvaluateResult.Success,
                    ),
                )

            queries.append(
                MyQuery(
                    f"Query-{module_index}-{query_index}",
                    "",
                    GetExecutionStyle(query_index),
                    requirements,
                ),
            )

        modules.append(
            MyModule(
                f"Module-{module_index}",
                "",
                GetExecutionStyle(module_index),
                queries,
            ),
        )

    with DoneManager.Create(sys.stdout, "", line_prefix="") as dm:
        Execute(
            dm,
            modules,
            max_num_threads=1 if single_threaded else None,
        )

        assert dm.result == 0


# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "data",
    [
        (EvaluateResult.Error, -1, False, False),
        (EvaluateResult.Warning, 1, False, False),
        (EvaluateResult.Warning, -1, True, False),
        (EvaluateResult.Warning, 0, False, True),
    ],
)
def test_NotSuccess(data):
    test_result, expected_result, warnings_as_errors, ignore_warnings = data

    modules: list[Module] = []

    # ----------------------------------------------------------------------
    def GetExecutionStyle(index: int) -> ExecutionStyle:
        return ExecutionStyle.Parallel if index % 2 == 0 else ExecutionStyle.Sequential

    # ----------------------------------------------------------------------

    for module_index in range(5):
        queries: list[Query] = []

        for query_index in range(4):
            requirements: list[Requirement] = []

            for requirement_index in range(5):
                requirements.append(
                    MyRequirement(
                        f"Requirement-{module_index}-{query_index}-{requirement_index}",
                        "",
                        GetExecutionStyle(requirement_index),
                        "",
                        "",
                        (test_result if requirement_index % 3 == 0 else EvaluateResult.Success),
                    ),
                )

            queries.append(
                MyQuery(
                    f"Query-{module_index}-{query_index}",
                    "",
                    GetExecutionStyle(query_index),
                    requirements,
                ),
            )

        modules.append(
            MyModule(
                f"Module-{module_index}",
                "",
                GetExecutionStyle(module_index),
                queries,
            ),
        )

    with DoneManager.Create(sys.stdout, "", line_prefix="") as dm:
        Execute(
            dm,
            modules,
            warnings_as_errors_module_names=(
                set() if not warnings_as_errors else {module.name for module in modules}
            ),
            ignore_warnings_module_names=(
                set() if not ignore_warnings else {module.name for module in modules}
            ),
        )

        assert dm.result == expected_result
