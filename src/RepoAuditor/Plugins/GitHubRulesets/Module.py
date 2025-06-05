# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubRulesetModule object for the GitHubRulesets plugin."""

from pathlib import Path
from typing import Any, Optional
import typer
import requests

from dbrownell_Common.TyperEx import TypeDefinitionItemType
from dbrownell_Common.Types import override

from RepoAuditor.Module import ExecutionStyle, Module

from .Query import RulesetQuery


class GitHubRulesetModule(Module):
    """Module that validates GitHub repository rulesets."""

    def __init__(self) -> None:
        super().__init__(
            "GitHubRuleset",
            "Validates GitHub repository rulesets.",
            ExecutionStyle.Parallel,
            [RulesetQuery()],
            requires_explicit_include=True,
        )

    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        return {
            "url": (
                str,
                typer.Option(
                    ...,
                    help="[REQUIRED] GitHub repository URL (e.g., https://github.com/owner/repo).",
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

    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Generate the initial data to be used in the `dynamic_args`, such as session info, etc."""
        github_url = dynamic_args.get("url")
        github_pat = dynamic_args.get("pat")

        if not github_url:
            msg = "Error: GitHub repository URL is required."
            raise RuntimeError(msg)

        session = _GitHubSession(github_url, github_pat)
        dynamic_args["session"] = session

        return dynamic_args


class _GitHubSession:
    """Session used to communicate with GitHub APIs for ruleset validation."""

    def __init__(
        self,
        github_url: str,
        github_pat: Optional[str],
    ) -> None:
        from urllib.parse import urlparse

        self.github_url = github_url.strip("/")
        self.github_pat = github_pat

        url_parts = urlparse(self.github_url)
        path_parts = url_parts.path.split("/")

        if len(path_parts) != 3:
            msg = f"'{github_url}' is not a valid GitHub repository URL."
            raise ValueError(msg)

        _, username, repo = path_parts

        if url_parts.netloc.lower() in ["github.com", "www.github.com"]:
            api_url = f"https://api.github.com/repos/{username}/{repo}"
            is_enterprise = False
        else:
            api_url = f"{url_parts.scheme}://{url_parts.netloc}/api/v3/orgs/{username}/repos/{repo}"
            is_enterprise = True

        self.github_username = username
        self.github_repository = repo
        self.api_url = api_url
        self.is_enterprise = is_enterprise

        self.headers = {
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
        }

        if github_pat:
            potential_file = Path(github_pat)
            if potential_file.is_file():
                with potential_file.open("r") as f:
                    github_pat = f.read().strip()

            self.headers["Authorization"] = f"Bearer {github_pat}"

    def request(self, method: str, endpoint: str, *args, **kwargs) -> requests.Response:
        """Send a request to the GitHub API."""

        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        response = requests.request(
            method, f"{self.api_url}{endpoint}", *args, timeout=10, headers=self.headers, **kwargs
        )
        response.raise_for_status()
        return response.json()
