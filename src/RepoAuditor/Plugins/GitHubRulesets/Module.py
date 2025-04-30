from pathlib import Path
from typing import Any, Optional
import typer

from dbrownell_Common.TyperEx import TypeDefinitionItemType
from dbrownell_Common.Types import override

from RepoAuditor.Module import ExecutionStyle, Module

from .RulesetQuery import RulesetQuery


class GitHubRulesetModule(Module):
    """Module that validates GitHub repository rulesets."""

    def __init__(self) -> None:
        super(GitHubRulesetModule, self).__init__(
            "GitHubRuleset",
            "Validates GitHub repository rulesets.",
            ExecutionStyle.Parallel,
            [RulesetQuery()],
            requires_explicit_include=True,
        )

    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            "url": (
                str,
                typer.Option(
                    ...,
                    help="[REQUIRED] GitHub repository URL (e.g., https://github.com/owner/repo).",
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
        github_url = dynamic_args.get("url", None)
        github_pat = dynamic_args.get("pat", None)

        if not github_url:
            print("Error: GitHub repository URL is required.")
            return None

        try:
            session = _GitHubSession(github_url, github_pat)
            dynamic_args["session"] = session
        except ValueError as e:
            print(f"Error creating GitHub session: {e}")
            return None

        return dynamic_args

    @override
    def Cleanup(self, dynamic_args: dict[str, Any]) -> None:
        """Clean up any resources created during execution."""
        print("Cleaning up GitHubRulesetModule resources...")
        super(GitHubRulesetModule, self).Cleanup(dynamic_args)


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
            raise ValueError(f"'{github_url}' is not a valid GitHub repository URL.")

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

    def request(self, method: str, endpoint: str, *args, **kwargs):
        """Send a request to the GitHub API."""
        import requests

        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        response = requests.request(
            method, f"{self.api_url}{endpoint}", headers=self.headers, *args, **kwargs
        )
        response.raise_for_status()
        return response.json()
