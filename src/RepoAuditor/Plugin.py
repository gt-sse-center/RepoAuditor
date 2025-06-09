# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the interface that Plugins must implement."""

import pluggy

from RepoAuditor import APP_NAME
from RepoAuditor.Module import Module


# ----------------------------------------------------------------------
@pluggy.HookspecMarker(APP_NAME)
def GetModule() -> Module:
    """Return a Module."""
    raise NotImplementedError("hookspec")  # pragma: no cover # noqa: EM101
