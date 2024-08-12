# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains Plugin functionality"""

import pluggy

from RepoAuditor import APP_NAME
from RepoAuditor.Module import Module

from .GitHub.Module import GitHubModule


# ----------------------------------------------------------------------
@pluggy.HookimplMarker(APP_NAME)
def GetModule() -> Module:
    return GitHubModule()
