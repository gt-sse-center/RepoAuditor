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

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import extension  # type: ignore[import-untyped]

from .Impl.ParallelSequentialProcessor import ExecutionStyle


# ----------------------------------------------------------------------
class EvaluateResult(Enum):
    """Result of evaluating a Requirement against a set of data."""

    DoesNotApply = auto()
    Success = auto()
    Warning = auto()
    Error = auto()


# ----------------------------------------------------------------------
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
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        description: str,
        style: ExecutionStyle,
        resolution_template: str,
        rationale_template: str,
        *,
        requires_explicit_include: bool = False,  # If True, the requirement must be explicitly included on the command line
    ) -> None:
        self.name = name
        self.description = description
        self.style = style

        self.resolution_template = resolution_template
        self.rationale_template = rationale_template

        self.requires_explicit_include = requires_explicit_include

    # ----------------------------------------------------------------------
    @extension
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Returns information about dynamic arguments that the requirement can consume (often from the command line)."""

        # No dynamic arguments by default
        return {}

    # ----------------------------------------------------------------------
    def Evaluate(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> "Requirement.EvaluateInfo":
        result, context, provide_rationale = self._EvaluateImpl(query_data, requirement_args)

        if result == EvaluateResult.Error:
            return Requirement.EvaluateInfo(
                result,
                context,
                self.resolution_template.format(**query_data),
                self.rationale_template.format(**query_data) if provide_rationale else None,
                self,
            )

        return Requirement.EvaluateInfo(result, context, None, None, self)

    # ----------------------------------------------------------------------
    # |
    # |  Private Methods
    # |
    # ----------------------------------------------------------------------
    @abstractmethod
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> tuple[EvaluateResult, Optional[str], bool]:
        """Perform the actual evaluation"""
