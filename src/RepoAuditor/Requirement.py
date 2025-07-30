# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains types used when creating Requirements."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import Any, Optional

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import extension  # type: ignore[import-untyped]

from RepoAuditor.Impl.ParallelSequentialProcessor import ExecutionStyle


# ----------------------------------------------------------------------
class EvaluateResult(Enum):
    """Result of evaluating a Requirement against a set of data."""

    DoesNotApply = auto()
    Success = auto()
    Warning = auto()
    Error = auto()


class ReturnCode(IntEnum):
    """Various return codes for operations, indicating success, failure, warning, etc."""

    SUCCESS = 0
    ERROR = -1
    WARNING = 1
    DOESNOTAPPLY = 2


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
    @dataclass(frozen=True)
    class EvaluateImplResult:
        """Result of evaluating a Requirement."""

        result: EvaluateResult
        context: Optional[str]
        provide_resolution: bool = field(kw_only=True, default=False)
        provide_rationale: bool = field(kw_only=True, default=False)

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
        requires_explicit_include: bool = False,
    ) -> None:
        """Initialize the requirement with the given name, description, and style.

        If `requires_explicit_include` is True, the requirement must be explicitly included on the command line.
        """
        self.name = name
        # Use description template so we can update this description for each requirement
        self.description_template = description
        # Use the description as is as backup
        self.description = description
        self.style = style

        self.resolution_template = resolution_template
        self.rationale_template = rationale_template

        self.requires_explicit_include = requires_explicit_include

    # ----------------------------------------------------------------------
    @extension
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Return information about dynamic arguments that the requirement can consume (often from the command line)."""

        # No dynamic arguments by default
        return {}

    # ----------------------------------------------------------------------
    def Evaluate(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> "Requirement.EvaluateInfo":
        """Evaluate the requirements given the query data and specific arguments."""
        result_info = self._EvaluateImpl(query_data, requirement_args)

        # Fill in templates in description string
        self.description = self.description_template.format(**query_data)

        if result_info.result == EvaluateResult.Error:
            return Requirement.EvaluateInfo(
                result_info.result,
                result_info.context,
                (self.resolution_template.format(**query_data) if result_info.provide_resolution else None),
                (self.rationale_template.format(**query_data) if result_info.provide_rationale else None),
                self,
            )

        return Requirement.EvaluateInfo(result_info.result, result_info.context, None, None, self)

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
    ) -> "Requirement.EvaluateImplResult":
        """Perform the actual evaluation."""
