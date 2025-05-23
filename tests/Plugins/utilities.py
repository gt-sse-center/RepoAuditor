# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Helper utilities for Github tests"""

from git import Repo

import re
from typing import Match
from dbrownell_Common.TestHelpers.StreamTestHelpers import ScrubDuration


# ----------------------------------------------------------------------
def ScrubSpaces(content: str) -> str:
    """
    Function to remove variable spaces after a match with a Github URL from a string.
    """

    def replace_func(match: Match) -> str:
        return match.group("scrubbed_github_url") + "<scrubbed-space>"

    return re.sub(
        r"(?P<scrubbed_github_url>'<scrubbed-github-url>')(\s+)",
        replace_func,
        content,
    )


# ----------------------------------------------------------------------
def ScrubGithubUrl(content: str) -> str:
    """
    Function to replace the GitHub username and (possibly) alternative repository name with the default one.
    """

    def replace_func(_: Match) -> str:
        return "'<scrubbed-github-url>'"

    return re.sub(
        r"('https?:\/\/.+')",
        replace_func,
        content,
    )


def ScrubDurationGithuburlAndSpaces(content: str) -> str:
    """Scrub the duration, GitHub urls, and variable spaces from the content."""
    scrubbed_duration = ScrubDuration(content)
    replaced_github_url = ScrubGithubUrl(scrubbed_duration)
    scrubbed_spaces = ScrubSpaces(replaced_github_url)
    return scrubbed_spaces


def GetGithubUrl(remote_name: str = "origin") -> str:
    """Get the Github username, repository and URL from the current git repository."""
    repo = Repo(__file__, search_parent_directories=True)

    # Get the URL for the remote specified by `remote_name`.
    repo_url = getattr(repo.remotes, remote_name).url

    if repo_url.startswith("git@"):
        # If the URL starts with 'git@', it is an SSH URL.
        # Convert it to HTTPS format.
        repo_url = repo_url.replace(":", "/").replace("git@", "https://")

    return repo_url.split(".git")[0]
