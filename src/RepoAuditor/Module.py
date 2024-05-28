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

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]

from .Impl.ParallelSequentialProcessor import ParallelSequentialProcessor
from .Query import EvaluateResult, ExecutionStyle, OnStatusFunc, Query, StatusInfo


# ----------------------------------------------------------------------
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
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        description: str,
        style: ExecutionStyle,
        queries: list[Query],
        *,
        requires_explicit_include: bool = False,  # If True, the module must be explicitly included on the command line
    ) -> None:
        self.name = name
        self.description = description
        self.style = style
        self.queries = queries
        self.requires_explicit_include = requires_explicit_include

    # ----------------------------------------------------------------------
    def GetNumRequirements(self) -> int:
        return sum(len(query.requirements) for query in self.queries)

    # ----------------------------------------------------------------------
    def ProcessRequirements(
        self,
        included_names: set[str],
        excluded_names: set[str],
    ) -> None:
        query_index = 0

        while query_index < len(self.queries):
            query = self.queries[query_index]

            requirement_index = 0

            while requirement_index < len(query.requirements):
                requirement = query.requirements[requirement_index]

                if (
                    requirement.requires_explicit_include and requirement.name not in included_names
                ) or (requirement.name in excluded_names):
                    query.requirements.pop(requirement_index)
                    continue

                requirement_index += 1

            if not query.requirements:
                self.queries.pop(query_index)
                continue

            query_index += 1

    # ----------------------------------------------------------------------
    @abstractmethod
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Returns information about dynamic arguments that the module can consume (often from the command line)."""

        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    @abstractmethod
    def GenerateInitialData(
        self,
        dynamic_args: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """\
        Augments data beyond data initially encountered (for example, on the command line).

        Return None to indicate that the Module cannot be evaluated. Raise an
        exception to indicate that the command line data is invalid.
        """

        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    def Evaluate(
        self,
        module_data: dict[str, Any],
        requirement_data: dict[str, Any],
        status_func: OnStatusFunc,
        *,
        max_num_threads: Optional[int] = None,
    ) -> list[list["Module.EvaluateInfo"]]:
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
                requirement_data,
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
