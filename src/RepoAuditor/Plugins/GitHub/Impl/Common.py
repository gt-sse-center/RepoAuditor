# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains common functionality that is used across different components."""

from RepoAuditor.Requirement import EvaluateResult, Requirement


# ----------------------------------------------------------------------
def CreateIncompleteDataResult(pat_value_exists: bool) -> Requirement.EvaluateImplResult:  # noqa: FBT001
    """Create an incomplete data result.

    Checks if the PAT value is `None` to generate additional message info.

    Args:
        pat_value_exists (bool): The value of the Personal Access Token.

    Returns:
        Requirement.EvaluateImplResult: A warning result notifying the user of an incomplete result.

    """
    error_message = "Incomplete data was encountered."
    if pat_value_exists:
        error_message += "\nPlease update the permissions of the GitHub PAT."
    else:
        error_message += "\nGitHub PAT was not provided. Please provide the PAT."

    return Requirement.EvaluateImplResult(
        EvaluateResult.Warning,
        error_message,
    )
