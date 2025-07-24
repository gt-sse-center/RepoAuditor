# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubBaseModule object."""

from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import requests
import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]

from RepoAuditor.Module import Module


# ----------------------------------------------------------------------
class GitHubBaseModule(Module):
    """Module for common GitHub settings which can be inherited by various GitHub plugins."""

    # ----------------------------------------------------------------------
    # The __init__ method is inherited from the Module class
    # and does not need to be overriden.

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
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
            "branch": (
                str,
                typer.Option(
                    None,
                    help="Branch to evaluate. The default branch will be used if not specified.",
                ),
            ),
        }

    # ----------------------------------------------------------------------
    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Generate the initial data to be used in the `dynamic_args`, such as session info, etc."""
        # Read the PAT (if provided) as a filename or a value.
        # This also decouples the PAT reading logic from the GitHubSession class (which may be mocked for testing).
        github_pat = dynamic_args.get("pat")
        if github_pat:
            potential_file = Path(github_pat)
            if potential_file.is_file():
                with potential_file.open("r") as f:
                    github_pat = f.read().strip()
        # Re-assign github_pat so it can be used within the subclassed modules.
        dynamic_args["pat"] = github_pat

        # Create a GitHub API session
        dynamic_args["session"] = _GitHubSession(dynamic_args["url"], dynamic_args.get("pat"))

        return dynamic_args


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _GitHubSession(requests.Session):
    """Session used to communicate with GitHub APIs."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        github_url: str,
        github_pat: Optional[str],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.headers.update(
            {
                "X-GitHub-Api-Version": "2022-11-28",
                "Accept": "application/vnd.github+json",
            },
        )

        if github_pat:
            self.headers["Authorization"] = f"Bearer {github_pat}"

        github_url = github_url.removesuffix("/")

        url_parts = urlparse(github_url)
        path_parts = url_parts.path.split("/")

        # The URL should be of the form <github_server>/<username>/<repo>
        if len(path_parts) != 3:  # noqa: PLR2004
            msg = f"'{github_url}' is not a valid GitHub repository URL."
            raise ValueError(msg)

        _, username, repo = path_parts

        if url_parts.netloc.lower() in ["github.com", "www.github.com"]:
            api_url = f"https://api.github.com/repos/{username}/{repo}"
            is_enterprise = False
        else:
            api_url = f"{url_parts.scheme}://{url_parts.netloc}/api/v3/repos/{username}/{repo}"
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
    ) -> requests.Response:
        if url and not url.startswith("/"):
            url = f"/{url}"

        return super().request(
            method,
            f"{self.api_url}{url}",
            *args,
            **kwargs,
        )
