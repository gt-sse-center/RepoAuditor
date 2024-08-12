# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubModule object"""

from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import requests
import typer

from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Module import ExecutionStyle, Module

from .StandardQuery import StandardQuery


# ----------------------------------------------------------------------
class GitHubModule(Module):  # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super(GitHubModule, self).__init__(
            "GitHub",
            "Validates GitHub configuration settings.",
            ExecutionStyle.Parallel,
            [
                StandardQuery(),
            ],
            requires_explicit_include=True,
        )

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            "url": (
                str,
                typer.Option(
                    ...,
                    help="[REQUIRED] Github URL (e.g. https://github.com/gt-sse-center/RepoAuditor)",
                ),
            ),
            "pat": (
                str,
                typer.Option(
                    None,
                    help="GitHub Personal Access Token (PAT) or path to a local file containing the PAT.",
                ),
            ),
        }

    # ----------------------------------------------------------------------
    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:
        dynamic_args["session"] = _GitHubSession(dynamic_args["url"], dynamic_args.get("pat", None))

        return dynamic_args


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _GitHubSession(requests.Session):
    """Session used to communicate with GitHub APIs"""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        github_url: str,
        github_pat: Optional[str],
        *args,
        **kwargs,
    ) -> None:
        super(_GitHubSession, self).__init__(*args, **kwargs)

        self.headers.update(
            {
                "X-GitHub-Api-Version": "2022-11-28",
                "Accept": "application/vnd.github+json",
            },
        )

        if github_pat:
            potential_file = Path(github_pat)

            if potential_file.is_file():
                with potential_file.open("r") as f:
                    github_pat = f.read().strip()

            self.headers["Authorization"] = f"Bearer {github_pat}"

        if github_url.endswith("/"):
            github_url = github_url[:-1]

        url_parts = urlparse(github_url)
        path_parts = url_parts.path.split("/")

        if len(path_parts) != 3:
            raise ValueError(f"'{github_url}' is not a valid GitHub repository URL.")

        _, username, repo = path_parts

        if url_parts.netloc.lower() in ["github.com", "www.github.com"]:
            api_url = f"https://api.github.com/repos/{username}/{repo}"
            is_enterprise = False
        else:
            api_url = f"{url_parts.scheme}://{url_parts.netloc}/api/v3/orgs/{username}/repos/{repo}"
            is_enterprise = True

        self.github_url = github_url
        self.github_pat = github_pat
        self.github_username = username
        self.github_repository = repo
        self.api_url = api_url
        self.is_enterprise = is_enterprise
        self.has_pat = bool(github_pat)

    # ----------------------------------------------------------------------
    def request(
        self,
        method: str,
        url: str,
        *args,
        **kwargs,
    ):
        if url and not url.startswith("/"):
            url = f"/{url}"

        return super(_GitHubSession, self).request(
            method,
            f"{self.api_url}{url}",
            *args,
            **kwargs,
        )
