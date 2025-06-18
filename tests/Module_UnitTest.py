# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit test for Module.py"""

import copy
from typing import Optional, cast
from unittest.mock import Mock

import pytest
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.TestHelpers.StreamTestHelpers import GenerateDoneManagerAndContent
from dbrownell_Common.Types import override

from RepoAuditor.Module import *
from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
class MyModule(Module):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        description: str,
        style: ExecutionStyle,
        queries: list[Query],
        *,
        produce_data: bool,
        requires_explicit_include: bool = False,
    ) -> None:
        super().__init__(
            name,
            description,
            style,
            queries,
            requires_explicit_include=requires_explicit_include,
        )

        self.produce_data = produce_data

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {}

    # ----------------------------------------------------------------------
    @override
    def GenerateInitialData(
        self,
        dynamic_args: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        if self.produce_data is False:
            return None

        assert not dynamic_args

        dynamic_args["produce_data"] = self.produce_data
        dynamic_args["one"] = 1
        dynamic_args["two"] = 2
        dynamic_args["three"] = 3
        dynamic_args["four"] = 4
        dynamic_args["module_data"] = self.name

        return dynamic_args


# ----------------------------------------------------------------------
class MyQuery(Query):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        style: ExecutionStyle,
        requirements: list[Requirement],
        *,
        produce_data: bool,
    ) -> None:
        super().__init__(name, style, requirements)

        self.produce_data = produce_data

    # ----------------------------------------------------------------------
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        if not self.produce_data:
            return None

        module_data["query_data"] = self.name

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
        evaluate_result: EvaluateResult,
        *,
        requires_explicit_include: bool = False,
    ) -> None:
        super().__init__(
            name,
            description,
            style,
            resolution_template,
            rationale_template,
            requires_explicit_include=requires_explicit_include,
        )

        self.evaluate_result = evaluate_result

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        return Requirement.EvaluateImplResult(
            self.evaluate_result,
            None,
            provide_resolution=True,
            provide_rationale=True,
        )


# ----------------------------------------------------------------------
def test_Construct():
    name = Mock()
    description = Mock()
    style = Mock()
    queries = Mock()
    produce_data = Mock()
    requires_explicit_include = Mock()

    module = MyModule(
        name,
        description,
        style,
        queries,
        produce_data=produce_data,
        requires_explicit_include=requires_explicit_include,
    )

    assert module.name is name
    assert module.description is description
    assert module.style is style
    assert module.queries is queries
    assert module.produce_data is produce_data
    assert module.requires_explicit_include is requires_explicit_include


# ----------------------------------------------------------------------
requirementA1 = MyRequirement(
    "RequirementA1",
    "The first requirement for A",
    ExecutionStyle.Sequential,
    "{one} -- {two} -- {query_data} -- {module_data}",
    "{three} -- {four} -- {query_data} -- {module_data}",
    EvaluateResult.Success,
    requires_explicit_include=True,
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
    requires_explicit_include=True,
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
    ExecutionStyle.Parallel,
    [requirementA1, requirementA2, requirementA3, requirementA4],
    produce_data=True,
)

queryB = MyQuery(
    "QueryB",
    ExecutionStyle.Parallel,
    [requirementB1, requirementB2, requirementB3, requirementB4],
    produce_data=True,
)

queryC = MyQuery(
    "QueryC",
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

    initial_data = module.GenerateInitialData({})
    assert initial_data is not None

    results = module.Evaluate(
        initial_data,
        {},
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
    query_c_expected_results = [
        Module.EvaluateInfo(
            result=EvaluateResult.DoesNotApply,
            context="QueryC did not return valid data.",
            rationale="",
            resolution="",
            requirement=requirement,
            query=queryC,
            module=module,
        )
        for requirement in queryC.requirements
    ]
    for idx, result in enumerate(results[2]):
        assert result == query_c_expected_results[idx]

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

    initial_data = module.GenerateInitialData({})
    assert initial_data is None


# ----------------------------------------------------------------------
def test_Module_SingleParallel():
    """Test parallel execution of the module when only 1 query is present."""
    # Since we have only one query with parallel execution style,
    # it should default to sequential processing.
    module = MyModule(
        "MyModule",
        "The only module",
        ExecutionStyle.Sequential,
        [queryA],
        produce_data=True,
    )

    status_func = Mock()

    initial_data = module.GenerateInitialData({})
    results = module.Evaluate(
        initial_data,
        {},
        status_func,
        max_num_threads=1,
    )
    assert results[0][0].result == EvaluateResult.Success
    assert results[0][0].context is None
    assert results[0][0].resolution is None
    assert results[0][0].rationale is None
    assert results[0][0].requirement is requirementA1
    assert results[0][0].query is queryA
    assert results[0][0].module is module


# ----------------------------------------------------------------------
def test_ProvidedDoneManager():
    """Test for when a DoneManager is provided to the ParallelSequentialProcessor."""
    module = MyModule(
        "MyModule",
        "The only module",
        ExecutionStyle.Sequential,
        [queryA],
        produce_data=True,
    )
    dm_and_sink = GenerateDoneManagerAndContent()
    dm = cast(DoneManager, next(dm_and_sink))
    result = ParallelSequentialProcessor(module.queries, lambda query: (0, []), dm)
    assert isinstance(result, list)


# ----------------------------------------------------------------------
class TestProcessRequriements:
    # ----------------------------------------------------------------------
    def test_NoIncludes(self):
        module = MyModule(
            "MyModule",
            "",
            ExecutionStyle.Sequential,
            [copy.deepcopy(queryA)],
            produce_data=False,
        )

        assert module.GetNumRequirements() == 4
        assert module.queries

        module.ProcessRequirements(
            set(),
            set(),
        )

        # The requires_explicit_include requirements should be removed
        assert module.GetNumRequirements() == 3
        assert module.queries

        module.ProcessRequirements(set(), {"RequirementA2"})
        assert module.GetNumRequirements() == 2
        assert module.queries

        module.ProcessRequirements(set(), {"RequirementA3", "RequirementA4"})
        assert module.GetNumRequirements() == 0
        assert not module.queries

    # ----------------------------------------------------------------------
    def test_WithIncludes(self):
        module = MyModule(
            "MyModule",
            "",
            ExecutionStyle.Sequential,
            [copy.deepcopy(queryA)],
            produce_data=False,
        )

        assert module.GetNumRequirements() == 4
        assert module.queries

        module.ProcessRequirements(
            {"RequirementA1"},
            set(),
        )

        assert module.GetNumRequirements() == 4
        assert module.queries

        module.ProcessRequirements(
            {"RequirementA1"},
            {"RequirementA3", "RequirementA4"},
        )

        assert module.GetNumRequirements() == 2
        assert module.queries
