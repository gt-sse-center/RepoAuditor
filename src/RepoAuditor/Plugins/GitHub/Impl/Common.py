# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains common functionality that is used across different components."""

from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
def CreateIncompleteDataResult() -> Requirement.EvaluateImplResult:
    """Create an incomplete data result."""
    return Requirement.EvaluateImplResult(
        EvaluateResult.Warning,
        "Incomplete data was encountered; please provide the GitHub PAT or update the PAT's permissions if one was provided.",
    )
