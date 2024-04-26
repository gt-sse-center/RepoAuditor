# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the Module object and types used in its definition"""

import threading

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from .Impl.ParallelSequentialProcessor import ParallelSequentialProcessor
from .Query import EvaluateResult, ExecutionStyle, OnStatusFunc, Query, StatusInfo


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Module(ABC):
    """A collection of Queries that operate on a consistent set of data."""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class EvaluateInfo(Query.EvaluateInfo):
        """Information associated with evaluating a Module against a set of data."""

        module: "Module"

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    name: str
    description: str
    style: ExecutionStyle

    queries: list[Query]

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def GetNumRequirements(self) -> int:
        return sum(len(query.requirements) for query in self.queries)

    # ----------------------------------------------------------------------
    def Evaluate(
        self,
        status_func: OnStatusFunc,
        *,
        max_num_threads: Optional[int] = None,
    ) -> list[list["Module.EvaluateInfo"]]:
        num_requirements = self.GetNumRequirements()

        module_data = self._GetData()
        if module_data is None:
            status_func(num_requirements, 0, 0, 0, num_requirements)
            return []

        status_info = StatusInfo()
        status_info_lock = threading.Lock()

        # ----------------------------------------------------------------------
        def EvaluateQuery(
            query: Query,
        ) -> tuple[int, list[Module.EvaluateInfo]]:
            query_data = query.GetData(dict(module_data))
            if query_data is None:
                with status_info_lock:
                    status_info.num_completed += len(query.requirements)
                    status_info.num_does_not_apply += len(query.requirements)

                    status_func(*status_info.__dict__.values())
                    return 0, []

            prev_query_status_info = StatusInfo()

            # ----------------------------------------------------------------------
            def OnQueryStatus(
                num_completed: int,
                num_success: int,
                num_error: int,
                num_warning: int,
                num_does_not_apply: int,
            ) -> None:
                with status_info_lock:
                    status_info.num_completed += (
                        num_completed - prev_query_status_info.num_completed
                    )
                    status_info.num_success += num_success - prev_query_status_info.num_success
                    status_info.num_error += num_error - prev_query_status_info.num_error
                    status_info.num_warning += num_warning - prev_query_status_info.num_warning
                    status_info.num_does_not_apply += (
                        num_does_not_apply - prev_query_status_info.num_does_not_apply
                    )

                    status_func(*status_info.__dict__.values())

                prev_query_status_info.num_completed = num_completed
                prev_query_status_info.num_success = num_success
                prev_query_status_info.num_error = num_error
                prev_query_status_info.num_warning = num_warning
                prev_query_status_info.num_does_not_apply = num_does_not_apply

            # ----------------------------------------------------------------------

            evaluate_infos = query.Evaluate(
                query_data,
                OnQueryStatus,
                max_num_threads=max_num_threads,
            )

            return_code = 0

            for evaluate_info in evaluate_infos:
                if evaluate_info.result == EvaluateResult.Error:
                    return_code = -1
                    break

                elif evaluate_info.result == EvaluateResult.Warning:
                    return_code = 1

            return (
                return_code,
                [
                    Module.EvaluateInfo(
                        **{
                            **{"module": self},
                            **evaluate_info.__dict__,
                        },
                    )
                    for evaluate_info in evaluate_infos
                ],
            )

        # ----------------------------------------------------------------------

        return ParallelSequentialProcessor(
            self.queries,
            EvaluateQuery,
            max_num_threads=max_num_threads,
        )

    # ----------------------------------------------------------------------
    # |
    # |  Private Methods
    # |
    # ----------------------------------------------------------------------
    @abstractmethod
    def _GetData(self) -> Optional[dict[str, Any]]:
        """Returns the data required by Queries associated with this Module."""
