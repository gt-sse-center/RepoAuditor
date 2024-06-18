# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains common functionality that is used across different components."""

from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
def CreateIncompleteDataResult() -> Requirement.EvaluateImplResult:
    return Requirement.EvaluateImplResult(
        EvaluateResult.Warning,
        "Incomplete data was encountered; please provide the GitHub PAT.",
    )
