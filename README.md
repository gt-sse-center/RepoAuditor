# RepoAuditor - README

**Project:**
[![License](https://img.shields.io/github/license/gt-sse-center/RepoAuditor?color=dark-green)](https://github.com/gt-sse-center/RepoAuditor/blob/master/LICENSE)

**Package:**
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/repoauditor?color=dark-green)](https://pypi.org/project/repoauditor/)
[![PyPI - Version](https://img.shields.io/pypi/v/repoauditor?color=dark-green)](https://pypi.org/project/repoauditor/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/repoauditor)](https://pypistats.org/packages/repoauditor)

**Development:**
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![CI](https://github.com/gt-sse-center/RepoAuditor/actions/workflows/CICD.yml/badge.svg)](https://github.com/gt-sse-center/RepoAuditor/actions/workflows/CICD.yml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/davidbrownell/2f9d770d13e3a148424f374f74d41f4b/raw/RepoAuditor_code_coverage.json)](https://github.com/gt-sse-center/RepoAuditor/actions)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/gt-sse-center/RepoAuditor?color=dark-green)](https://github.com/gt-sse-center/RepoAuditor/commits/main/)

<!-- Content above this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

## Contents

- [Installation](#installation)
- [Overview](#overview)
  - [How to use RepoAuditor](#how-to-use-repoauditor)
  - [Personal Access Token](#personal-access-token-pat)
  - [Example Usage](#example-usage)
  - [Config File](#config-file)
- [Development](#development)
- [Additional Information](#additional-information)
- [License](#license)

## Installation

We recommend using [uv](https://docs.astral.sh/uv/#uv) since it can install `RepoAuditor` as a tool via `uvx` into a sandbox environment for quick use.
This lets you directly run `RepoAuditor`.

```sh
uvx RepoAuditor
```

Alternatively, yuou can install `RepoAuditor` via `uv` or `pip`.
`uv` is preferred to `pip` since it creates and manages a virtual environment.

| Installation Method | Command |
| --- | --- |
| Via [uv](https://github.com/astral-sh/uv) | `uv add repoauditor` |
| Via [pip](https://pip.pypa.io/en/stable/) | `pip install repoauditor` |

## Overview

### How to use RepoAuditor

<!-- Content below this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

Once installed, you can invoke the following to verify if `RepoAuditor` is installed correctly:

```shell
uvx RepoAuditor --version
```

and you should see something like

```shell
RepoAuditor vX.X.X
```

To get a list of command line options, you can run

```shell
uvx RepoAuditor --help
```

### Personal Access Token (PAT)

The most common use case for `RepoAuditor` would be to audit a GitHub repository.
In order to allow `RepoAuditor` to read the repository, you first need to generate a Personal Access Token or **PAT**.

Please refer to the [GitHub documentation on Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for details about a `Fine-grained PAT` which we will be using.

To generate the Fine-grained PAT, we perform the following steps:

1. Go to `Settings -> Developer settings -> Personal Access Token -> Fine-grained tokens`.
2. Click on `Generate new token`.
3. Give the token a name and a description.
4. Set an appropriate expiration date.
5. Under `Repository Access`, select `All repositories`.
6. For permissions, we need to go to `Repository permissions`.
7. Enable the following permissions:
    - Read-Write access to `Contents`.
    - Read access to `Administration` and `Secret scanning alerts`.
8. Click on `Generate token`.
9. Copy the generated string. This is your PAT.
10. Save the PAT to a convenient location on your machine (such as your hime directory `~/`) in the file `PAT.txt`.

The path to the `PAT.txt` will be passed into `RepoAuditor`. E.g.

```shell
uvx RepoAuditor --GitHub-pat ~/PAT.txt
```

### Example Usage

With the above generated PAT file, you can now run `RepoAuditor` on your GitHub repository.

As a general example, we will use the [python-helloworld](https://github.com/dbarnett/python-helloworld) repository.

> **NOTE** You need to fork the repository since your default PAT only has access to repos under your account.

To run `RepoAuditor`, we can enter the following in the command-line:

```shell
uvx RepoAuditor --include GitHub \
  --GitHub-url https://github.com/<username>/python-helloworld \
  --GitHub-pat ~/PAT.txt
```

`RepoAuditor` will generate a series of messages describing all the issues in the repository, along with the rationale behind them and the steps for resolution.

### Config File

`RepoAuditor` accepts both a set of flags as well as a configuratin YAML file.

The configuration (or config) file can make usage easier by recording preferences as well as facilitating sharing of enforced requirements within an organization.
We have provided a sample configuration file called [default_config.yaml](https://github.com/gt-sse-center/RepoAuditor/blob/main/default_config.yaml), which can be used as:
```shell
uvx run RepoAuditor --config default_config.yaml
```

## Development

Please visit [Contributing](https://github.com/gt-sse-center/RepoAuditor/blob/main/CONTRIBUTING.md) and [Development](https://github.com/gt-sse-center/RepoAuditor/blob/main/DEVELOPMENT.md) for information on contributing to this project.

## Additional Information

Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md](https://github.com/gt-sse-center/RepoAuditor/blob/main/CODE_OF_CONDUCT.md) | Information about the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md](https://github.com/gt-sse-center/RepoAuditor/blob/main/CONTRIBUTING.md) | Information about contributing to this project. |
| Development | [DEVELOPMENT.md](https://github.com/gt-sse-center/RepoAuditor/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md](https://github.com/gt-sse-center/RepoAuditor/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md](https://github.com/gt-sse-center/RepoAuditor/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md](https://github.com/gt-sse-center/RepoAuditor/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |

## License

RepoAuditor is licensed under the <a href="https://choosealicense.com/licenses/MIT/" target="_blank">MIT</a> license.
