"""Determine if a GitHub Actions workflow should run based on the last run time and commits since then."""

# /// script
# requires-python = ">=3.13"
# dependencies = ["dbrownell_Common", "requests", "rich", "typer"]
# ///

import datetime
import re
import textwrap

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import requests
import typer

from dbrownell_Common.InflectEx import inflect
from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from dbrownell_Common import SubprocessEx
from rich import print as pretty_print
from rich.table import Table
from typer.core import TyperGroup


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):  # noqa: D101
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs) -> list[str]:  # noqa: ARG002, D102
        return list(self.commands.keys())


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
def _ExtractTimeDeltaCommandLineArgument(value: str) -> datetime.timedelta:
    """Extract a timedelta from a string in the format 'HH:MM:SS'."""

    match = re.match(r"(\d+):(\d+):(\d+)", value)
    if not match:
        message = f"'{value}' is not a valid time format; use 'HH:MM:SS' format."
        raise typer.BadParameter(message)

    hours, minutes, seconds = map(int, match.groups())
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)


# ----------------------------------------------------------------------
@app.command("EntryPoint", help=__doc__, no_args_is_help=True)
def EntryPoint(  # noqa: D103
    github_api_url: Annotated[
        str,
        typer.Argument(help="The GitHub API url"),
    ],
    workflow_name: Annotated[
        str,
        typer.Argument(help="The name of the workflow to query"),
    ],
    max_idle_time: Annotated[
        str,
        typer.Option(
            "--max-idle-time",
            callback=_ExtractTimeDeltaCommandLineArgument,
            help="Indicate that the workflow should run if it has been idle for longer than this time period. ",
        ),
    ] = "24:00:00",  # 1 day
    github_pat: Annotated[
        str | None,
        typer.Option(
            "--pat",
            help="The GitHub Personal Access Token (PAT) to use for authentication.",
        ),
    ] = None,
    *,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    assert isinstance(max_idle_time, datetime.timedelta), max_idle_time

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        should_run = _ShouldRun(dm, github_api_url, workflow_name, max_idle_time, github_pat)

        if should_run is True:
            dm.WriteLine("\n*** The CI process should run! ***\n")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class _GitHubSession(requests.Session):
    """Session used to communicate with GitHub APIs."""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        github_api_url: str,
        github_pat: str | None,
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
            potential_file = Path(github_pat)

            if potential_file.is_file():
                with potential_file.open("r") as f:
                    github_pat = f.read().strip()

            self.headers["Authorization"] = f"Bearer {github_pat}"

        self.github_api_url = github_api_url.removesuffix("/")

    # ----------------------------------------------------------------------
    def request(
        self,
        method: str,
        url: str,
        *args,
        **kwargs,
    ) -> requests.Response:
        url = url.removeprefix("/")

        return super().request(
            method,
            f"{self.github_api_url}/{url}",
            *args,
            **kwargs,
        )


# ----------------------------------------------------------------------
@dataclass
class _CommitInfo:
    """Information about a commit."""

    name: str
    email: str
    hash: str
    date: datetime.datetime
    subject: str


# ----------------------------------------------------------------------
def _ShouldRun(
    dm: DoneManager,
    github_api_url: str,
    workflow_name: str,
    max_idle_time: datetime.timedelta,
    github_pat: str | None,
) -> bool | None:
    session = _GitHubSession(github_api_url, github_pat)

    # Get the workflow ID
    workflow_id = _GetWorkflowId(dm, session, workflow_name)
    if workflow_id is None:
        return None

    last_run_time = _GetLastWorkflowRunTime(dm, session, workflow_id, max_idle_time)
    if last_run_time is None:
        return True

    commits = _GetCommits(dm, last_run_time)
    if not commits:
        return False

    # Display the commits
    table = Table()

    table.add_column("Commit Hash")
    table.add_column("Author")
    table.add_column("Commit Time")
    table.add_column("Subject")

    for commit in commits:
        table.add_row(commit.hash, f"{commit.name} <{commit.email}>", commit.date.isoformat(), commit.subject)

    pretty_print(table)

    return True


# ----------------------------------------------------------------------
def _GetWorkflowId(
    dm: DoneManager,
    session: requests.Session,
    workflow_name: str,
) -> int | None:
    workflow_id: int | None = None

    with dm.Nested(
        "Getting workflow ID...",
        lambda: None if workflow_id is None else f"Workflow ID: {workflow_id}",
    ) as nested_dm:
        page_index = 1

        while workflow_id is None:
            response = session.get("actions/workflows", params={"page": page_index})
            page_index += 1

            response.raise_for_status()

            data = response.json()["workflows"]
            if not data:
                nested_dm.WriteError(f"The id for workflow '{workflow_name}' was not found.\n")
                break

            for workflow in data:
                if workflow["name"] == workflow_name:
                    workflow_id = workflow["id"]
                    break

    return workflow_id


# ----------------------------------------------------------------------
def _GetLastWorkflowRunTime(
    dm: DoneManager,
    session: requests.Session,
    workflow_id: int,
    max_idle_time: datetime.timedelta,
) -> datetime.datetime | None:
    workflow_runs: list[dict] = []

    with dm.Nested(
        "Getting workflow runs...",
        lambda: "{} found".format(inflect.no("workflow", len(workflow_runs))),
    ):
        query_params = {
            "page": 1,
            "per_page": 100,
            "created": f">{datetime.datetime.now(datetime.timezone.utc) - max_idle_time}",
        }

        while True:
            response = session.get("actions/runs", params=query_params)
            query_params["page"] += 1

            response.raise_for_status()

            data = response.json()
            data = data["workflow_runs"]
            if not data:
                break

            for run in data:
                if run["workflow_id"] == workflow_id and run["status"] == "completed":
                    run["created_at"] = datetime.datetime.fromisoformat(run["created_at"])
                    workflow_runs.append(run)

    if not workflow_runs:
        return None

    workflow_runs.sort(key=lambda run: run["created_at"], reverse=True)
    return workflow_runs[0]["created_at"]


# ----------------------------------------------------------------------
def _GetCommits(
    dm: DoneManager,
    last_run_time: datetime.datetime,
) -> list[_CommitInfo] | None:
    commits: list[_CommitInfo] = []

    with dm.Nested(
        f"Looking for commits since '{last_run_time}'...",
        lambda: "{} found".format(inflect.no("commit", len(commits))),
    ) as nested_dm:
        separator = "<__sep__>"

        # List all of the git changes that have been introduced since the last run
        git_log_format: list[str] = [
            "%H",  # Commit hash
            "%an",  # Author name
            "%ae",  # Author email
            "%cI",  # Commit date
            "%s",  # Commit subject
        ]

        git_log_format_str = separator.join(git_log_format)

        command_line = f'git log --first-parent --format="{git_log_format_str}" --since="{last_run_time}"'

        result = SubprocessEx.Run(command_line)
        if result.returncode != 0:
            nested_dm.WriteError(
                textwrap.dedent(
                    f"""\
                    Git command: {command_line}
                    Result:
                    {result.output}
                    """,
                ),
            )
            return None

        regex = re.compile(
            r"^(?P<hash>.+?){escaped_sep}(?P<name>.+?){escaped_sep}(?P<email>.+?){escaped_sep}(?P<date>.+?){escaped_sep}(?P<subject>.+)$".format(
                escaped_sep=re.escape(separator),
            ),
        )

        for line in result.output.splitlines():
            match = regex.match(line)
            assert match, line

            commits.append(
                _CommitInfo(
                    name=match.group("name"),
                    email=match.group("email"),
                    hash=match.group("hash"),
                    date=datetime.datetime.fromisoformat(match.group("date")),
                    subject=match.group("subject"),
                ),
            )

        return commits


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()
