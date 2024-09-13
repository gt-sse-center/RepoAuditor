# Contribution Guidelines

Additional information is available at the following locations.

| Topic | Description | Location |
| --- | --- | --- |
| Code of Conduct | How we welcome others to this community. | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Development Activities | How we create software in this community. | [DEVELOPMENT.md](DEVELOPMENT.md) |
| Security | How to report vulnerabilities in our software. | [SECURITY.md](SECURITY.md) |

# Bug Reports
If you experience a problem with our software, please visit [issues](https://github.com/gt-sse-center/RepoAuditor/issues) and create a `Bug report`.

# Feature Requests
If you would like to suggest a new feature for our software, please visit [issues](https://github.com/gt-sse-center/RepoAuditor/issues) and create a `Feature request`.

# Issue Labels
We use these labels to help us track and manage `Bug reports` and `Feature requests`.

| Label | Description |
| --- | --- |
| `bug` | Something isn't working. |
| `enhancement` | New feature or request. |
| `help wanted` | Extra attention is needed. |
| `good first issue` | Good for newcomers. |
| `documentation` | Improvements or additions to documentation. |

## General information
<!-- [BEGIN] General Information -->
For specific proposals, please provide them as [pull requests](https://github.com/coreinfrastructure/best-practices-badge/pulls) or [issues](https://github.com/coreinfrastructure/best-practices-badge/issues) via our [GitHub site](https://github.com/gt-sse-center/RepoAuditor).
<!-- [END] General Information -->

The [DEVELOPMENT.md](DEVELOPMENT.md) file explains how to install the program locally (highly recommended if you're going to make code changes). It also provides information useful for making changes and validating them locally before submitting a pull request.

### Pull requests and different branches recommended
<!-- [BEGIN] Pull Requests and Branches -->
Pull requests are preferred, since they are specific. For more about how to create a pull request, see https://help.github.com/articles/using-pull-requests/.

We recommend creating different branches for different (logical) changes, and creating a pull request into the `main` branch when you're done. See the GitHub documentation on [creating branches](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) and [using pull requests](https://help.github.com/articles/using-pull-requests/).
<!-- [END] Pull Requests and Branches -->

### How we handle proposals
<!-- [BEGIN] Proposals -->
We use GitHub to track proposed changes via its [issue tracker](https://github.com/coreinfrastructure/best-practices-badge/issues) and [pull requests](https://github.com/coreinfrastructure/best-practices-badge/pulls). Specific changes are proposed using those mechanisms. Issues are assigned to an individual, who works and then marks it complete. If there are questions or objections, the conversation of that issue or pull request is used to resolve it.
<!-- [END] Proposals -->

### We are proactive
In general we try to be proactive to detect and eliminate mistakes and vulnerabilities as soon as possible, and to reduce their impact when they do happen. We use a defensive design and coding style to reduce the likelihood of mistakes, a variety of tools that try to detect mistakes early, and an automatic test suite with significant coverage. We also release the software as open source software so others can review it.

Since early detection and impact reduction can never be perfect, we also try to detect and repair problems during deployment as quickly as possible. This is especially true for security issues; see our [security information](#vulnerability-reporting-security-issues) for more information.

## Vulnerability reporting (security issues)
Please privately report vulnerabilities you find so we can fix them!

See [SECURITY.md](SECURITY.md) for information on how to privately report vulnerabilities.

## Acknowledgements

This Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org), version 1.0.0, available at [http://contributor-covenant.org/version/1/0/0/](http://contributor-covenant.org/version/1/0/0/)
