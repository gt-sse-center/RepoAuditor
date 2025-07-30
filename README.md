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

## Overview

`RepoAuditor` is a tool which audits repositories for best practices.

If you're running an open-source repository, there are many steps involved in being open-source beyond making your repository public.

In order to make your repository both friendly to maintainers and contributors, you will want to enable/disable some settings (e.g. require reviews, status checks pass), or you may be missing certains files (like `LICENSE` or `CODE_OF_CONDUCT`) that prevent adoption of your project.

`RepoAuditor` can check and audit your repository so that all the right settings and content are available to make your open-source repository high-quality, even if you are new to maintaining one.

E.g. check if various files for maintaining community standards are available:

```shell
uvx repoauditor --include CommunityStandards \
    --CommunityStandards-url https://github.com/gt-sse-center/RepoAuditor \
    --verbose
```

This will check if your open-source repository has files like a License, Code of Conduct, README, Code Owners, etc.

We have set `RepoAuditor` to have defaults which match with best practices in open-source communities, however they can all be overrided.

For more information on how to use `RepoAuditor` and its available features, please refer to the documentation below.

## Documentation

Please refer to the documentation hosted [here](docs/index.md).

## Development

Please visit [Contributing](https://github.com/gt-sse-center/RepoAuditor/blob/main/docs/CONTRIBUTING.md) and [Development](https://github.com/gt-sse-center/RepoAuditor/blob/docs/development.md) for information on contributing to this project.

## Additional Information

Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Information about the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Information about contributing to this project. |
| Development | [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md](GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md](MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md](SECURITY.md) | Information about how to privately report security issues associated with this project. |

## License

RepoAuditor is licensed under the <a href="https://choosealicense.com/licenses/MIT/" target="_blank">MIT</a> license.
