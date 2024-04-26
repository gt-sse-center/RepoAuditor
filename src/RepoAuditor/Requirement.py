# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains types used when creating Requirements."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any, Optional


from .Impl.ParallelSequentialProcessor import ExecutionStyle


# ----------------------------------------------------------------------
class EvaluateResult(Enum):
    """Result of evaluating a Requirement against a set of data."""

    DoesNotApply = auto()
    Success = auto()
    Warning = auto()
    Error = auto()


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Requirement(ABC):
    """A single requirement that can be evaluated against a set of data."""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class EvaluateInfo:
        """Information associated with evaluating a Requirement against a set of data."""

        result: EvaluateResult
        context: Optional[str]

        resolution: Optional[str]
        rationale: Optional[str]

        requirement: "Requirement"

    # ----------------------------------------------------------------------
    # |
    # |  Public Data
    # |
    # ----------------------------------------------------------------------
    name: str
    description: str
    style: ExecutionStyle

    resolution_template: str
    rationale_template: str

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def Evaluate(
        self,
        query_data: dict[str, Any],
    ) -> "Requirement.EvaluateInfo":
        result, context = self._EvaluateImpl(query_data)

        if result in [EvaluateResult.DoesNotApply, EvaluateResult.Success]:
            return Requirement.EvaluateInfo(result, context, None, None, self)

        return Requirement.EvaluateInfo(
            result,
            context,
            self.resolution_template.format(**query_data),
            self.rationale_template.format(**query_data),
            self,
        )

    # ----------------------------------------------------------------------
    # |
    # |  Private Methods
    # |
    # ----------------------------------------------------------------------
    @abstractmethod
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
    ) -> tuple[EvaluateResult, Optional[str]]:
        """Perform the actual evaluation"""
