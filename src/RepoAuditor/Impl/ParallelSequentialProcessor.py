# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains functionality to process items in parallel and/or sequentially."""

from enum import auto, Enum
from typing import Callable, cast, Optional, TypeVar

from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator  # type: ignore[import-untyped]


# ----------------------------------------------------------------------
class ExecutionStyle(Enum):
    """Controls the way in which a Requirement, Query, and Module can be processed."""

    Sequential = auto()
    Parallel = auto()


# ----------------------------------------------------------------------
ItemType = TypeVar("ItemType")
OutputType = TypeVar("OutputType")


def ParallelSequentialProcessor(
    items: list[ItemType],
    calculate_result_func: Callable[[ItemType], tuple[int, OutputType]],
    dm: Optional[DoneManager] = None,
    *,
    max_num_threads: Optional[int] = None,
) -> list[OutputType]:
    if dm is None:
        with DoneManager.Create(StreamDecorator(None), "", line_prefix="") as dm:
            return _Impl(
                dm,
                items,
                calculate_result_func,
                max_num_threads,
            )

    return _Impl(
        dm,
        items,
        calculate_result_func,
        max_num_threads,
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _Impl(
    dm: DoneManager,
    items: list[ItemType],
    calculate_result_func: Callable[[ItemType], tuple[int, OutputType]],
    max_num_threads: Optional[int],
) -> list[OutputType]:
    # Divide the items into those that can be run in parallel and those that must be run sequentially
    parallel: list[tuple[int, ItemType]] = []
    sequential: list[tuple[int, ItemType]] = []

    for index, item in enumerate(items):
        execution_style = item.style  # type: ignore

        if execution_style == ExecutionStyle.Parallel:
            parallel.append((index, item))
        elif execution_style == ExecutionStyle.Sequential:
            sequential.append((index, item))
        else:
            assert False, execution_style  # pragma: no cover

    if len(parallel) == 1:
        sequential.append(parallel[0])
        parallel = []

    # Calculate the results
    results: list[Optional[OutputType]] = [None] * len(items)

    # ----------------------------------------------------------------------
    def Execute(
        results_index: int,
        item: ItemType,
    ) -> ExecuteTasks.TransformResultComplete:
        return_code, result = calculate_result_func(item)

        assert results[results_index] is None
        results[results_index] = result

        return ExecuteTasks.TransformResultComplete(None, return_code)

    # ----------------------------------------------------------------------

    if parallel:
        ExecuteTasks.TransformTasks(
            dm,
            "Processing",
            [
                ExecuteTasks.TaskData(item.name, (results_index, item))  # type: ignore
                for results_index, item in parallel
            ],
            lambda context, status: Execute(*context),
            max_num_threads=max_num_threads,
        )

    for sequential_index, (results_index, item) in enumerate(sequential):
        with dm.Nested(
            "Processing '{}' ({} of {})...".format(
                item.name,  # type: ignore
                sequential_index + 1 + len(parallel),
                len(items),
            ),
        ):
            Execute(results_index, item)

    assert not any(result is None for result in results), results
    return cast(list[OutputType], results)
