# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the Query object and types used in its definition"""

import threading

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Protocol

from .Impl.ParallelSequentialProcessor import ParallelSequentialProcessor
from .Requirement import EvaluateResult, ExecutionStyle, Requirement


# ----------------------------------------------------------------------
class OnStatusFunc(Protocol):
    def __call__(
        self,
        num_completed: int,
        num_success: int,
        num_error: int,
        num_warning: int,
        num_does_not_apply: int,
    ) -> None: ...


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Query(ABC):
    """A collection of Requirements that operate on a consistent set of data."""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class EvaluateInfo(Requirement.EvaluateInfo):
        """Information associated with evaluating a Query against a set of data."""

        query: "Query"

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    name: str
    description: str
    style: ExecutionStyle

    requirements: list[Requirement]

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    @abstractmethod
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Returns the data object augmented with information required by the Requirements associated with this Query."""

    # ----------------------------------------------------------------------
    def Evaluate(
        self,
        query_data: dict[str, Any],
        status_func: OnStatusFunc,
        *,
        max_num_threads: Optional[int] = None,
    ) -> list["Query.EvaluateInfo"]:
        status_info = StatusInfo()
        status_info_lock = threading.Lock()

        status_func(*status_info.__dict__.values())

        # ----------------------------------------------------------------------
        def EvaluateRequirement(
            requirement: Requirement,
        ) -> tuple[int, Query.EvaluateInfo]:
            result_info = requirement.Evaluate(query_data)
            return_code = 0

            with status_info_lock:
                status_info.num_completed += 1

                if result_info.result == EvaluateResult.DoesNotApply:
                    status_info.num_does_not_apply += 1
                elif result_info.result == EvaluateResult.Success:
                    status_info.num_success += 1
                elif result_info.result == EvaluateResult.Error:
                    status_info.num_error += 1
                    return_code = -1
                elif result_info.result == EvaluateResult.Warning:
                    status_info.num_warning += 1
                    return_code = 1
                else:
                    assert False, result_info.result  # pragma: no cover

                status_func(*status_info.__dict__.values())

            return (
                return_code,
                Query.EvaluateInfo(
                    **{
                        **{"query": self},
                        **result_info.__dict__,
                    },
                ),
            )

        # ----------------------------------------------------------------------

        return ParallelSequentialProcessor(
            self.requirements,
            EvaluateRequirement,
            max_num_threads=max_num_threads,
        )


# ----------------------------------------------------------------------
class StatusInfo:
    """Class used to store information required by OnStatusFunc."""

    # ----------------------------------------------------------------------
    def __init__(self):
        self.num_completed: int = 0
        self.num_success: int = 0
        self.num_error: int = 0
        self.num_warning: int = 0
        self.num_does_not_apply: int = 0
