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
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
- [License](#license)

## Overview
TODO: Complete this section

### How to use RepoAuditor

The most convenient way to use RepoAuditor is via a github action

1. Create a fine-grained Personal Access Token (PAT)
    * The PAT should be under the same user / org that owns the repository
    * Make sure the PAT has access to either all repositories, or select at least this repository
    * Grant the following permissions:
        1. Administration: Read-only
        1. Contents: Read/write
        1. Metadata: Read-only

2. Create a repository secret called `REPO_AUDITOR_PAT` whose contents is the PAT.

2. Create a `.github/workflows/RepoAuditor.yml` file with the following contents:
    ```yml
    name: RepoAuditor

    on: 
    workflow_dispatch:

    jobs:
    audit-repo:
        runs-on: ubuntu-latest
        steps:
        - uses: gt-sse-center/RepoAuditor@action-v0.2.1
            with:
            github_pat: ${{ secrets.REPO_AUDITOR_PAT }}
    ```

<!-- Content below this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

## Installation

| Installation Method | Command |
| --- | --- |
| Via [uv](https://github.com/astral-sh/uv) | `uv add repoauditor` |
| Via [pip](https://pip.pypa.io/en/stable/) | `pip install repoauditor` |

### Verifying Signed Artifacts
Artifacts are signed and validated using [py-minisign](https://github.com/x13a/py-minisign) and the public key in the file `./minisign_key.pub`.

To verify that an artifact is valid, visit [the latest release](https://github.com/gt-sse-center/RepoAuditor/releases/latest) and download the `.minisign` signature file that corresponds to the artifact, then run the following command, replacing `<filename>` with the name of the artifact to be verified:

`uv run --with py-minisign python -c "import minisign; minisign.PublicKey.from_file('minisign_key.pub').verify_file('<filename>')"`

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
