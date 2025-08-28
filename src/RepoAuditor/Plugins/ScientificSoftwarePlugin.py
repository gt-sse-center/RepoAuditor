# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains Plugin functionality."""

import pluggy

from RepoAuditor import APP_NAME
from RepoAuditor.Module import Module
from RepoAuditor.Plugins.ScientificSoftware.Module import ScientificSoftwareModule


# ----------------------------------------------------------------------
@pluggy.HookimplMarker(APP_NAME)
def GetModule() -> Module:
    """Return Scientific Software Module."""
    return ScientificSoftwareModule()
