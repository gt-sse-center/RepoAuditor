# Writing a Custom Plugin

RepoAuditor allows for extensibility by using a plugin system powered by [pluggy](https://pluggy.readthedocs.io/en/stable/).

On this page, you will learn the steps involved to develop custom, 3rd party plugins to extend RepoAuditor's functionality for your own use cases.

## Setup

To setup, create a new repository. We will call ours `ReadmeCheck` and we will use it to check if a repository has a `README.md` file.
We know this is a bit redundant but it lays the groundwork for this tutorial.

Follow the below commands to setup the basic skeleton project.

<!-- termynal -->
```sh
$ mkdir ReadmeCheck && cd ReadmeCheck
$ touch pyproject.toml README.md
$ mkdir ReadmeCheck
$ touch ReadmeCheck/__init__.py
```

We first start off by creating a very simple `pyproject.toml` file.

```toml title="pyproject.toml"
[project]
name = "ReadmeCheck"
description = "Custom plugin tutorial for RepoAuditor"
readme = "README.md"
authors = [
    { name = "Scientific Software Engineering Center at Georgia Tech", email = "sse-center@gatech.edu" },
]
requires-python = ">= 3.10"
dependencies = [
    "dbrownell-common>=0.16.0",
    "gitpython>=3.1.44",
    "RepoAuditor>=0.4.4",
]
version = "0.0.0"
classifiers = [
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.10",
]

[project.license]
text = "MIT"

[project.entry-points.RepoAuditor]
ReadmCheckPlugin = "ReadmeCheck.Plugin"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Plugin Components

For any RepoAuditor plugin, we need 4 files:

1. `Requirement.py`: Contains the class which inherits from `Requirement`, with the logic to actually check if the requirement is fulfilled.
2. `Query.py`: Has a class which inherits from `Query` and obtains the necessary data which is then passed to the requirement(s).
3. `Module.py`: A file with a class which inherits from `Module` and defines the dynamic arguments and which queries to execute for obtaining necessary data.
4. `Plugin.py`: Tells `pluggy` how to load the plugin so RepoAuditor can see it.

The files would be organized as:

```sh
$ tree
.
├── README.md
├── ReadmeCheck
│   ├── Module.py
│   ├── Plugin.py
│   ├── Query.py
│   ├── Requirement.py
│   └── __init__.py
└── pyproject.toml
```

### Requirement

To define a requirement, we define a class which inherits from `Requirement` and implements three methods:

1. `__init__(self) -> None`: The constructor.
2. `GetDynamicArgDefinitions(self, argument_separator: str) -> dict[str, TypeDefinitionItemType]`: A method which defines requirement specific dynamic arguments.
3. `_EvaluateImpl(self, query_data: dict[str, Any], requirement_args: dict[str, Any], ) -> Requirement.EvaluateImplResult`: The logic for verifying the requirement.

The definition for the `Requirement.py` file would be the following. Please see the inline comments for details about specific lines of code.

```python title="ReadmeCheck/Requirement.py"
"""Contains the Readme object."""

import textwrap
from pathlib import Path
from typing import Any

import typer
from dbrownell_Common.TyperEx import \
    TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]
from RepoAuditor.Requirement import EvaluateResult, ExecutionStyle, Requirement


class ReadmeRequirement(Requirement):
    """Requirement to validate a repository's README."""

    def __init__(self) -> None:
        super().__init__(
            name="Readme",
            description="Validates if the repository has a README.",
            style=ExecutionStyle.Parallel,

            # This is the template for the instructions to resolve
            # a failure caused by this requirement.
            resolution_template=textwrap.dedent(
                """\
                Add a README file to the repository.
                """, ),

            # This is the template for the rationale behind why this
            # requirement is good to have.
            rationale_template=textwrap.dedent(
                """\
                A README file helps users understand the project.
                """, ),

            # Flag which decides if an explicit include from the
            # command line is required to enable this requirement.
            requires_explicit_include=False,
        )

        # Flag deciding if the requirement is enabled by default.
        # Here the default is set to True, but this can be a constructor argument.
        # There might be a case where you wish to opt-out of checking for the
        # README by default, e.g. the docs exist in a separate wiki or service,
        # in which case `self.enabled_by_default` can be set to False.
        self.enabled_by_default: bool = True

        # The dynamic_arg_name is used in defining the dynamic
        # argument `ReadmeCheck-no-Readme`.
        # We use `no` since the requirement is enabled by default.
        # It is possible that an organization does not care about having a README (perhaps the docs are stored on a wiki),
        # in that case, specifying `--ReadmeCheck-no-Readme` will disable this check.
        self.dynamic_arg_name: str = "no"

    @override
    def GetDynamicArgDefinitions(
            self,
            argument_separator: str) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""

        # Defines a dynamic argument `ReadmeCheck-no-Readme` which if enabled
        # allows the requirement to pass if no README file is available.
        return {
            f"{self.dynamic_arg_name}{argument_separator}{self.name}": (
                bool,
                typer.Option(
                    default=False,
                    help="Allow missing README.",
                ),
            ),
        }

    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        """Implementation of the reqiurement evaluation.

        query_data: The data obtained from the query class (detailed next).
        requirement_args: Reqiurement specific dynamic arguments.
        """

        # Flag to check if the file exists.
        check_exists: bool = self.enabled_by_default

        # Check if the dynamic argument is provided,
        # which toggles the check flag
        if requirement_args.get(self.dynamic_arg_name, False):
            check_exists = not check_exists

        # Get full file path in temporary repo directory and
        # check if it exists.
        # This checks both upper case and lower case variants
        full_file_path = Path(query_data["repo_dir"].name) / "README.md"

        # If check flag is enabled, we perform the check.
        # The repository directory is in `query_data[repo_dir]`
        # thanks to the Query.py file.
        if check_exists:

            # If the README file exists, return success.
            if full_file_path.exists():
                return Requirement.EvaluateImplResult(
                    EvaluateResult.Success,
                    "README found inside the repository",
                )

            # Else return error.
            return Requirement.EvaluateImplResult(
                EvaluateResult.Error,
                "No README file found.",
                provide_resolution=True,
                provide_rationale=True,
            )

        # Else check if README does not exist.
        else:
            # If the README file exists, return error.
            if full_file_path.exists():
                return Requirement.EvaluateImplResult(
                    EvaluateResult.Error,
                    "A README was found inside the repository",
                )
            
            # Else return success
            return Requirement.EvaluateImplResult(
                EvaluateResult.Success,
                "No README file was found as expected.",
                provide_resolution=True,
                provide_rationale=True,
            )


        # Requirement not enabled, so return DoesNotApply
        return Requirement.EvaluateImplResult(EvaluateResult.DoesNotApply,
                                              None)

```

### Query

The `Query.py` file has a class `ReadmeQuery` whose responsibility is to obtain the data needed by the requirement.
Since multiple requirements may need ths same data, the `ReadmeQuery` runs once to obtain the data and passes it to all the requirements, thus reducing redundant operations.

`ReadmeQuery` needs to inherit from `Query` and implement 2 methods:

1. `__init__(self) -> None`: The constructor.
2. `def GetData(self, module_data: dict[str, Any]) -> Optional[dict[str, Any]]`: The method which performs the act of obtaining the necessary data.

The `ReadmeQuery` file can thus be defined as:

```python title="ReadmeCheck/Query.py"
"""Contains the ReadmeQuery class."""

from tempfile import TemporaryDirectory
from typing import Any, Optional

from dbrownell_Common.Types import override  # type: ignore[import-untyped]
from RepoAuditor.Query import ExecutionStyle, Query

from ReadmeCheck.Requirement import ReadmeRequirement

class ReadmeQuery(Query):
    """Query with requirements that operate on a repository directory."""

    # ----------------------------------------------------------------------
    def __init__(self) -> None:
        super().__init__(
            "ReadmeQuery",
            ExecutionStyle.Parallel,

            # Note that we can specify multiple requirements here,
            # all of which will get the same queried data.
            [
                ReadmeRequirement(),
            ],
        )

    @override
    def GetData(
        self,
        module_data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        """Get the repository directory."""

        # Clone the git repository to a temp directory
        branch = module_data.get("branch", "main")
        temp_repo_dir = TemporaryDirectory()
        url = module_data["url"]

        # Import git.Repo here so that it is only imported
        # if the plugin is requested.
        from git import Repo

        # Use the Repo class to clone the repository
        Repo.clone_from(url, temp_repo_dir.name, branch=branch)

        # Record the path and the temp directory for later cleanup
        module_data["repo_dir"] = temp_repo_dir

        # This module_data is passed to each requirement as `query_data`.
        return module_data

```

### Module

The `Module.py` file is the final file needed for implementing functionality.
This file has a class which inherits from `Module` and sets up common dynamic arguments, such as the repository `url`, and the initial module data.

We are required to implement 3 methods:

1. `__init__(self) -> None`: The constructor.
2. `GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]`: A method which defines module-level arguments which can be specified at runtime.
3. `GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]`: A method that executes before the data queries are made. Allows one to set up proper permissions and defaults.

We define a class `ReadmeCheckModule` which implements these methods as

```python title="ReadmeCheck/Module.py"
"""Contains the ReadmeCheckModule object."""

from typing import Any, Optional

import typer
from dbrownell_Common.TyperEx import \
    TypeDefinitionItemType  # type: ignore[import-untyped]
from dbrownell_Common.Types import override  # type: ignore[import-untyped]
from RepoAuditor.Module import ExecutionStyle, Module

from ReadmeCheck.Query import ReadmeQuery


class ReadmeCheckModule(Module):
    """Module for validating presence of a README file."""

    def __init__(self) -> None:
        super().__init__(
            "ReadmeCheck",
            "Validates presence of README file.",
            ExecutionStyle.Parallel,

            # This architecture allows us to specify multiple queries,
            # each of which can run in parallel.
            [
                ReadmeQuery(),
            ],
            requires_explicit_include=True,
        )

    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        """Get the definitions for the arguments to this requirement."""
        # Here we define the URL which is used to get the repository data.
        return {
            "url": (
                str,
                typer.Option(
                    ...,
                    help=
                    "[REQUIRED] Github URL (e.g. https://github.com/gt-sse-center/RepoAuditor)",
                ),
            ),
        }

    @override
    def GenerateInitialData(
            self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Generate the initial data to be used in the `dynamic_args`, such as session info, etc."""
        # Nothing to do so we just return the dynamic_args.
        # In alternative cases, we can set up things like
        # the GitHub personal access token here.
        return dynamic_args

```

### Plugin

This is the easiest file, and has the code which tells `pluggy` how to load our custom plugin into `RepoAuditor`.

```python title="ReadmeCheck/Plugin.py"
"""Contains Plugin functionality."""

import pluggy
from RepoAuditor import APP_NAME
from RepoAuditor.Module import Module

from ReadmeCheck.Module import ReadmeCheckModule


@pluggy.HookimplMarker(APP_NAME)
def GetModule() -> Module:
    """Return ReadMeCheck Module."""
    return ReadmeCheckModule()
```

Here, we simply load the app name from `RepoAuditor` as `APP_NAME` and implement a `GetModule` function with the `@pluggy.HookimplMarker` decorator.

All the `GetModule` function has to do is return the appropriate module, a.k.a. `ReadmeCheckModule()`.

## Running the Plugin

At this point, we are ready to execute our custom plugin.

We start by installing the package locally.

<!-- termynal -->
```sh
$ uv pip install -e .
Resolved 25 packages in 13ms
      Built readmecheck @ file:///Users/gt-sse-center/gt-sse/ReadmeCheck
Prepared 1 package in 648ms
Uninstalled 1 package in 1ms
Installed 1 package in 2ms
 ~ readmecheck==0.0.0 (from file:///Users/gt-sse-center/gt-sse/ReadmeCheck)
```

After this, we simply call `RepoAuditor` and specify our custom module in the `--include` flag, which should yield the following result:

<!-- termynal -->
```sh
$ uv run repoauditor --include ReadmeCheck \
    --ReadmeCheck-url https://github.com/gt-sse-center/RepoAuditor
Processing 1 module...
  Processing 'ReadmeCheck' (1 of 1)...
  Processing 'ReadmeCheck' (1 of 1)...DONE! (0, 0:00:00.697564):00 ✅
DONE! (0, 0:00:00.697655)
╭─────────────────────────── ReadmeCheck ───────────────────────────╮
│                                                                   │
│ Validates presence of README file.                                │
│                                                                   │
│                                                                   │
│ Successful:     1 (100.00%)                                       │
│ Warnings:       0 (0.00%)                                         │
│ Errors:         0 (0.00%)                                         │
│ Skipped:        0 (0.00%)                                         │
│                                                                   │
│ ╭─ Metrics ─────────────────────────────────────────────────────╮ │
│ │                                                               │ │
│ │                                                               │ │
│ │ Successful:     1 (100.00%)                                   │ │
│ │ Warnings:       0 (0.00%)                                     │ │
│ │ Errors:         0 (0.00%)                                     │ │
│ │ Skipped:        0 (0.00%)                                     │ │
│ │                                                               │ │
│ ╰───────────────────────────────────────────────────────────────╯ │
│                                                                   │
╰───────────────────────────────────────────────────────────────────╯
```

This indicates that our plugin was successfully loaded and executed by `RepoAuditor`.

## Conclusion

In this tutorial, we learned how to write a custom plugin for `RepoAuditor`, and all the necessary modules and classes we need to implement our plugin.

While the plugin detailed here performs a very basic check for the README file, the tutorial demonstrated the steps needed to get started. Actual functionality can be customized as per the needs of an application or organization, and `RepoAuditor` can efficiently execute the plugin.
