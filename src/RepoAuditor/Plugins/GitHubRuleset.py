import pluggy

from RepoAuditor import APP_NAME
from RepoAuditor.Module import Module

from .GitHubRulesets.Module import GitHubRulesetModule


@pluggy.HookimplMarker(APP_NAME)
def GetModule() -> Module:
    return GitHubRulesetModule()