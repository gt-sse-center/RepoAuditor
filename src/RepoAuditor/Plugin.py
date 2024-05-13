# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Contains the interface that Plugins must implement"""

import pluggy

from RepoAuditor import APP_NAME

from .Module import Module


# ----------------------------------------------------------------------
@pluggy.HookspecMarker(APP_NAME)
def GetModule() -> Module:
    """Returns a Module"""
    raise Exception("hookspec")  # pragma: no cover
