# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Helper utilities for Github tests"""

import re
import sys
import textwrap
from pathlib import Path
from typing import Match

from dbrownell_Common.TestHelpers.StreamTestHelpers import ScrubDuration
from git import Repo


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

    try:
        # Get the URL for the remote specified by `remote_name`.
        repo_url = getattr(repo.remotes, remote_name).url
    except AttributeError as exc:
        # The `remote_name` does not exist, so we use a default.
        # Specifically for main repo CI.
        if remote_name == "origin":
            repo_url = "git@github.com:gt-sse-center/RepoAuditor.git"
        elif remote_name == "enterprise":
            repo_url = "git@github.gatech.edu:sse-center/RepoAuditor.git"
        else:
            # Invalid remote name so we throw exception
            raise exc

    if repo_url.startswith("git@"):
        # If the URL starts with 'git@', it is an SSH URL.
        # Convert it to HTTPS format.
        repo_url = repo_url.replace(":", "/").replace("git@", "https://")

    return repo_url.split(".git")[0]


def CheckPATFileExists(github_pat_filename: Path, github_url: str = "https://github.com"):
    """Check if PAT file exists, and give error message if not."""
    if not github_pat_filename.is_file():
        sys.stdout.write(
            textwrap.dedent(
                f"""\


            The filename '{github_pat_filename}' does not exist. Please create this file and add your GitHub Personal Access Token (PAT) to it.
            This git repository is configured to ignore the file so that it will never be included as part of a commit.

            To create a new token:

                1. Visit {github_url}/settings/tokens/new
                2. Ensure that 'repo' scope is checked
                3. Click 'Generate token'
                4. Copy the token to the clipboard
                5. Create the file '{github_pat_filename}'
                6. Paste the token into the created file
                7. Save the file and run these tests again.

            These tests query a repository on GitHub, but GitHub limits the number of concurrent requests made to a repository when a PAT is
            not provided. As a result, the tests will fail once the limit is reached.
            """,
            ),
        )

        sys.exit(-1)
