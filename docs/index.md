# RepoAuditor

`RepoAuditor` is a handy tool which audits repositories for best practices.

It helps maintain high-quality and consistent open-source repositories even if you are new to maintaining open-source software.

## Contents

- [Installation](#installation)
- [How to use RepoAuditor](#how-to-use)
- [Personal Access Token](PAT.md)
- [Example Usage](usage.md)
- [Config File](config_file.md)
- [Development](development)

## Installation

We recommend using [uv](https://docs.astral.sh/uv/#uv) since it can install `RepoAuditor` as a tool via `uvx` into a sandbox environment for quick use.
This lets you directly run `RepoAuditor`.

```sh
uvx RepoAuditor
```

Alternatively, you can install `RepoAuditor` via `uv` or `pip`.
`uv` is preferred to `pip` since it creates and manages a virtual environment.

| Installation Method | Command |
| --- | --- |
| Via [uv](https://github.com/astral-sh/uv) | `uv add repoauditor` |
| Via [pip](https://pip.pypa.io/en/stable/) | `pip install repoauditor` |

## How To Use

Once installed, you can invoke the following to verify if `RepoAuditor` is installed correctly:

```sh
uvx RepoAuditor --version
```

and you should see something like

```sh
RepoAuditor vX.X.X
```

To get a list of command line options, you can run

```sh
uvx RepoAuditor --help
```

In order to use `RepoAuditor` with GitHub, you will need a Personal Access Token (or PAT for short).

Let's go over how to [generate a PAT next](PAT.md).
