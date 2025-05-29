# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit test for Query.py"""

from unittest.mock import Mock

import pytest

from dbrownell_Common.Types import override

from RepoAuditor.Query import *


# ----------------------------------------------------------------------
def test_StatusInfo():
    status_info = StatusInfo()

    assert status_info.num_completed == 0
    assert status_info.num_success == 0
    assert status_info.num_error == 0
    assert status_info.num_warning == 0
    assert status_info.num_does_not_apply == 0

    # Fields must be in this exact order, as code relies on it
    # to easily call OnStatusFunc.
    assert list(StatusInfo().__dict__.keys()) == [
        "num_completed",
        "num_success",
        "num_error",
        "num_warning",
        "num_does_not_apply",
    ]


# ----------------------------------------------------------------------
class MyQuery(Query):
    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        module_data["new_attribute"] = "NEW"

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
        expected_result: EvaluateResult,
        context: Optional[str] = None,
    ) -> None:
        super().__init__(name, description, style, resolution_template, rationale_template)

        self.expected_result = expected_result
        self.context = context

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
            self.expected_result,
            self.context,
            provide_resolution=True,
            provide_rationale=True,
        )


# ----------------------------------------------------------------------
requirement1 = MyRequirement(
    "MyRequirement1",
    "The first requirement",
    ExecutionStyle.Sequential,
    "{one} -- {two} -- {new_attribute}",
    "{three} -- {four} -- {new_attribute}",
    EvaluateResult.Success,
    None,
)

requirement2 = MyRequirement(
    "MyRequirement2",
    "The second requirement",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {new_attribute}",
    "{three} -- {four} -- {new_attribute}",
    EvaluateResult.Success,
    None,
)

requirement3 = MyRequirement(
    "MyRequirement3",
    "The third requirement",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {new_attribute}",
    "{three} -- {four} -- {new_attribute}",
    EvaluateResult.DoesNotApply,
    None,
)

requirement4 = MyRequirement(
    "MyRequirement4",
    "The fourth requirement",
    ExecutionStyle.Sequential,
    "{one} -- {two} -- {new_attribute}",
    "{three} -- {four} -- {new_attribute}",
    EvaluateResult.Error,
    None,
)

requirement5 = MyRequirement(
    "MyRequirement5",
    "The fifth requirement",
    ExecutionStyle.Parallel,
    "{one} -- {two} -- {new_attribute}",
    "{three} -- {four} -- {new_attribute}",
    EvaluateResult.Warning,
    None,
)

my_query = MyQuery(
    "MyQuery",
    ExecutionStyle.Sequential,
    [
        requirement1,
        requirement2,
        requirement3,
        requirement4,
        requirement5,
    ],
)


# ----------------------------------------------------------------------`
def test_MyQueryConstruct():
    assert my_query.name == "MyQuery"
    assert my_query.style == ExecutionStyle.Sequential
    assert my_query.requirements == [
        requirement1,
        requirement2,
        requirement3,
        requirement4,
        requirement5,
    ]


# ----------------------------------------------------------------------
@pytest.mark.parametrize("single_threaded", [True, False])
def test_Evaluate(single_threaded):
    module_data = {"one": 1, "two": 2, "three": 3, "four": 4}

    query_data = my_query.GetData(dict(module_data))
    assert query_data is not None

    status_func = Mock()

    results = my_query.Evaluate(
        query_data,
        {},
        status_func,
        max_num_threads=1 if single_threaded else None,
    )

    assert len(results) == 5

    assert results[0].result == EvaluateResult.Success
    assert results[0].query is my_query
    assert results[0].requirement is requirement1
    assert results[0].context is None
    assert results[0].resolution is None
    assert results[0].rationale is None

    assert results[1].result == EvaluateResult.Success
    assert results[1].query is my_query
    assert results[1].requirement is requirement2
    assert results[1].context is None
    assert results[1].resolution is None
    assert results[1].rationale is None

    assert results[2].result == EvaluateResult.DoesNotApply
    assert results[2].query is my_query
    assert results[2].requirement is requirement3
    assert results[2].context is None
    assert results[2].resolution is None
    assert results[2].rationale is None

    assert results[3].result == EvaluateResult.Error
    assert results[3].query is my_query
    assert results[3].requirement is requirement4
    assert results[3].context is None
    assert results[3].resolution == "1 -- 2 -- NEW"
    assert results[3].rationale == "3 -- 4 -- NEW"

    assert results[4].result == EvaluateResult.Warning
    assert results[4].query is my_query
    assert results[4].requirement is requirement5
    assert results[4].context is None
    assert results[4].resolution is None
    assert results[4].rationale is None

    if single_threaded:
        assert [call_args.args for call_args in status_func.call_args_list] == [
            (0, 0, 0, 0, 0),
            (1, 1, 0, 0, 0),
            (2, 1, 0, 0, 1),
            (3, 1, 0, 1, 1),
            (4, 2, 0, 1, 1),
            (5, 2, 1, 1, 1),
        ]
