# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Unit test for Module.py"""

from dataclasses import dataclass, field
from unittest.mock import Mock

import pytest

from dbrownell_Common.Types import override

from RepoAuditor.Module import *
from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyModule(Module):
    produce_data: bool = field(kw_only=True)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GetData(self) -> Optional[dict[str, Any]]:
        if self.produce_data:
            return {"one": 1, "two": 2, "three": 3, "four": 4, "module_data": self.name}

        return None


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyQuery(Query):
    produce_data: bool = field(kw_only=True)

    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        if not self.produce_data:
            return None

        module_data["query_data"] = self.name
        return module_data


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class MyRequirement(Requirement):
    evaluate_result: EvaluateResult

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
    ) -> tuple[EvaluateResult, Optional[str]]:
        return self.evaluate_result, None


# ----------------------------------------------------------------------
def test_Construct():
    name = Mock()
    description = Mock()
    style = Mock()
    queries = Mock()
    produce_data = Mock()

    module = MyModule(name, description, style, queries, produce_data=produce_data)

    assert module.name is name
    assert module.description is description
    assert module.style is style
    assert module.queries is queries
    assert module.produce_data is produce_data


# ----------------------------------------------------------------------
requirementA1 = MyRequirement(
    "RequirementA1",
    "The first requirement for A",
    ExecutionStyle.Sequential,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

requirementA2 = MyRequirement(
    "RequirementA2",
    "The second requirement for A",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

requirementA3 = MyRequirement(
    "RequirementA3",
    "The third requirement for A",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Error,
)

requirementA4 = MyRequirement(
    "RequirementA4",
    "The fourth requirement for A",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

requirementB1 = MyRequirement(
    "RequirementB1",
    "The first requirement for B",
    ExecutionStyle.Sequential,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

requirementB2 = MyRequirement(
    "RequirementB2",
    "The second requirement for B",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

requirementB3 = MyRequirement(
    "RequirementB3",
    "The third requirement for B",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

requirementB4 = MyRequirement(
    "RequirementB4",
    "The fourth requirement for B",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
)

queryA = MyQuery(
    "QueryA",
    "The first query",
    ExecutionStyle.Parallel,
    [requirementA1, requirementA2, requirementA3, requirementA4],
    produce_data=True,
)

queryB = MyQuery(
    "QueryB",
    "The second query",
    ExecutionStyle.Parallel,
    [requirementB1, requirementB2, requirementB3, requirementB4],
    produce_data=True,
)

queryC = MyQuery(
    "QueryC",
    "The third query",
    ExecutionStyle.Sequential,
    [requirementA1, requirementA2, requirementA3],
    produce_data=False,
)


# ----------------------------------------------------------------------
@pytest.mark.parametrize("single_threaded", [True, False])
def test_Module(single_threaded):
    module = MyModule(
        "MyModule",
        "The only module",
        ExecutionStyle.Sequential,
        [queryA, queryB, queryC],
        produce_data=True,
    )

    status_func = Mock()

    results = module.Evaluate(
        status_func,
        max_num_threads=1 if single_threaded else None,
    )

    assert len(results) == 3

    # QueryA
    assert len(results[0]) == 4

    assert results[0][0].result == EvaluateResult.Success
    assert results[0][0].context is None
    assert results[0][0].resolution is None
    assert results[0][0].rationale is None
    assert results[0][0].requirement is requirementA1
    assert results[0][0].query is queryA
    assert results[0][0].module is module

    assert results[0][1].result == EvaluateResult.Success
    assert results[0][1].context is None
    assert results[0][1].resolution is None
    assert results[0][1].rationale is None
    assert results[0][1].requirement is requirementA2
    assert results[0][1].query is queryA
    assert results[0][1].module is module

    assert results[0][2].result == EvaluateResult.Error
    assert results[0][2].context is None
    assert results[0][2].resolution == "1 -- 2 -- QueryA -- MyModule"
    assert results[0][2].rationale == "3 -- 4 -- QueryA -- MyModule"
    assert results[0][2].requirement is requirementA3
    assert results[0][2].query is queryA
    assert results[0][2].module is module

    assert results[0][3].result == EvaluateResult.Success
    assert results[0][3].context is None
    assert results[0][3].resolution is None
    assert results[0][3].rationale is None
    assert results[0][3].requirement is requirementA4
    assert results[0][3].query is queryA
    assert results[0][3].module is module

    # QueryB
    assert len(results[1]) == 4

    assert results[1][0].result == EvaluateResult.Success
    assert results[1][0].context is None
    assert results[1][0].resolution is None
    assert results[1][0].rationale is None
    assert results[1][0].requirement is requirementB1
    assert results[1][0].query is queryB
    assert results[1][0].module is module

    assert results[1][1].result == EvaluateResult.Success
    assert results[1][1].context is None
    assert results[1][1].resolution is None
    assert results[1][1].rationale is None
    assert results[1][1].requirement is requirementB2
    assert results[1][1].query is queryB
    assert results[1][1].module is module

    assert results[1][2].result == EvaluateResult.Success
    assert results[1][2].context is None
    assert results[1][2].resolution is None
    assert results[1][2].rationale is None
    assert results[1][2].requirement is requirementB3
    assert results[1][2].query is queryB
    assert results[1][2].module is module

    assert results[1][3].result == EvaluateResult.Success
    assert results[1][3].context is None
    assert results[1][3].resolution is None
    assert results[1][3].rationale is None
    assert results[1][3].requirement is requirementB4
    assert results[1][3].query is queryB
    assert results[1][3].module is module

    # QueryC
    assert results[2] == []

    # Validate the notifications
    if single_threaded:
        assert [call_args.args for call_args in status_func.call_args_list] == [
            (0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0),
            (2, 1, 1, 0, 0),
            (3, 2, 1, 0, 0),
            (4, 3, 1, 0, 0),
            (4, 3, 1, 0, 0),
            (5, 4, 1, 0, 0),
            (6, 5, 1, 0, 0),
            (7, 6, 1, 0, 0),
            (8, 7, 1, 0, 0),
            (11, 7, 1, 0, 3),
        ]


# ----------------------------------------------------------------------
def test_ModuleNoData():
    module = MyModule(
        "MyModule",
        "The only module",
        ExecutionStyle.Sequential,
        [queryA, queryB, queryC],
        produce_data=False,
    )

    status_func = Mock()

    results = module.Evaluate(status_func)

    assert results == []
    assert [call_args.args for call_args in status_func.call_args_list] == [(11, 0, 0, 0, 11)]
