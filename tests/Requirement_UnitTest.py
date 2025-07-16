# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for Requirement.py"""

from unittest.mock import Mock

import pytest

from dbrownell_Common.Types import override

from RepoAuditor.Requirement import *


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
        *,
        requires_explicit_include: bool = False,
        provide_rationale: bool = True,
    ) -> None:
        super().__init__(
            name,
            description,
            style,
            resolution_template,
            rationale_template,
            requires_explicit_include=requires_explicit_include,
        )

        self.expected_result = expected_result
        self.context = context
        self._provide_rationale = provide_rationale

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
            provide_resolution=self.expected_result == EvaluateResult.Error,
            provide_rationale=self._provide_rationale,
        )


# ----------------------------------------------------------------------
def test_Construct():
    name = Mock()
    description = ""
    style = Mock()
    resolution_template = Mock()
    rationale_template = Mock()
    expected_result = Mock()
    context = Mock()
    requires_explicit_include = Mock()

    r = MyRequirement(
        name,
        description,
        style,
        resolution_template,
        rationale_template,
        expected_result,
        context,
        requires_explicit_include=requires_explicit_include,
    )

    assert r.name is name
    assert r.description is description
    assert r.style is style
    assert r.resolution_template is resolution_template
    assert r.rationale_template is rationale_template
    assert r.expected_result is expected_result
    assert r.context is context
    assert r.requires_explicit_include is requires_explicit_include


# ----------------------------------------------------------------------
def test_Success():
    requirement = MyRequirement(Mock(), Mock(), Mock(), Mock(), Mock(), EvaluateResult.Success, "testing")
    result_info = requirement.Evaluate({"key": "value"}, {})

    assert result_info.result == EvaluateResult.Success
    assert result_info.context == "testing"
    assert result_info.resolution is None
    assert result_info.rationale is None
    assert result_info.requirement is requirement


# ----------------------------------------------------------------------
def test_DoesNotApply():
    requirement = MyRequirement(Mock(), Mock(), Mock(), Mock(), Mock(), EvaluateResult.DoesNotApply, None)
    result_info = requirement.Evaluate({"key": "value"}, {})

    assert result_info.result == EvaluateResult.DoesNotApply
    assert result_info.context is None
    assert result_info.resolution is None
    assert result_info.rationale is None
    assert result_info.requirement is requirement


# ----------------------------------------------------------------------
def test_GetDynamicArgDefinitions():
    requirement = MyRequirement(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        EvaluateResult.Success,
        "testing",
    )

    assert requirement.GetDynamicArgDefinitions() == {}


# ----------------------------------------------------------------------
@pytest.mark.parametrize("provide_rationale", [True, False])
def test_Error(provide_rationale: bool):
    requirement = MyRequirement(
        Mock(),
        Mock(),
        Mock(),
        "{one} -- {two}",
        "{three} -- {four}",
        EvaluateResult.Error,
        "testing",
        provide_rationale=provide_rationale,
    )

    result_info = requirement.Evaluate({"one": "1", "two": "2", "three": "3", "four": "4"}, {"four": "FOUR"})

    assert result_info.result == EvaluateResult.Error
    assert result_info.context == "testing"
    assert result_info.resolution == "1 -- 2"
    assert result_info.rationale == ("3 -- 4" if provide_rationale else None)
    assert result_info.requirement is requirement


# ----------------------------------------------------------------------
def test_Warning():
    requirement = MyRequirement(
        Mock(),
        Mock(),
        Mock(),
        "{one} -- {two}",
        "{three} -- {four}",
        EvaluateResult.Warning,
        None,
    )

    result_info = requirement.Evaluate({"one": "1", "two": "2", "three": "3", "four": "4"}, {"four": "FOUR"})

    assert result_info.result == EvaluateResult.Warning
    assert result_info.context is None
    assert result_info.resolution is None
    assert result_info.rationale is None
    assert result_info.requirement is requirement


# ----------------------------------------------------------------------
