# Fork setup

| Step | Command Line | Additional Information |
| --- | --- | --- |
| 1. Fork the repository | -- | https://github.com/gt-sse-center/RepoAuditor/fork |
| 2. Create a PAT for your forked repository | -- | See [PAT setup instructions](README.md#personal-access-token-pat) |
| 3. Update your forked repository settings to match RepoAuditor's defaults | -- | 


# Local Development

## Enlistment

| Step | Command Line | Additional Information |
| --- | --- | --- |
| 1. Clone the repository locally. | `git clone https://github.com/gt-sse-center/RepoAuditor` | https://git-scm.com/docs/git-clone |
| 2. Install [uv](https://github.com/astral-sh/uv). | `curl -LsSf https://astral.sh/uv/install.sh \| sh` on macOS and Linux or <br/>`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` on Windows | https://docs.astral.sh |
| 3. Install dependencies. | `uv sync` | https://docs.astral.sh/uv/concepts/projects/sync |
| 4. Install [pre-commit](https://pre-commit.com/) hooks | `uv run pre-commit install` | https://pre-commit.com/#1-install-pre-commit |
| 5. If you wish to test against an enterprise server, add a remote named `enterprise` with the corresponding URL | E.g. `git remote add enterprise git@github.gatech.edu:sse-center/RepoAuditor.git` | |

## Development Activities

| Activity | Command Line | Description | Used During Local Development | Invoked by Continuous Integration |
| --- | --- | --- | :-: | :-: |
| Code Formatting | `uv run ruff format` or<br>`uv run ruff format --check` | Format source code using [ruff](https://github.com/astral-sh/ruff) based on settings in `pyproject.toml`. | :white_check_mark: | :white_check_mark: (via [pre-commit](https://pre-commit.com/)) |
| Static Code Analysis | `uv run ruff check` | Validate source code using [ruff](https://github.com/astral-sh/ruff) based on settings in `pyproject.toml`. | :white_check_mark: | :white_check_mark: (via [pre-commit](https://pre-commit.com/)) |
| Run pre-commit scripts | `uv run pre-commit run` | Run [pre-commit](https://pre-commit.com/) scripts based on settings in `.pre-commit-config.yaml`. | :white_check_mark: | :white_check_mark: |
| Automated Testing | `uv run pytest` or<br/>`uv run pytest --no-cov` | Run automated tests using [pytest](https://docs.pytest.org/) and extract code coverage using [coverage](https://coverage.readthedocs.io/) based on settings in `pyproject.toml`. | :white_check_mark: | :white_check_mark: |
| Semantic Version Generation | `uv run python -m AutoGitSemVer.scripts.UpdatePythonVersion ./src/RepoAuditor/__init__.py ./src` | Generate a new [Semantic Version](https://semver.org/) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored in `./src/RepoAuditor/__init__.py`. | | :white_check_mark: |
| Python Package Creation | `uv build` | Create a python package using [uv](https://github.com/astral-sh/uv) based on settings in `pyproject.toml`. Generated packages will be written to `./dist`. | | :white_check_mark: |
| Sign Artifacts | `uv run --with py-minisign python -c "import minisign; minisign.SecretKey.from_file(<temp_filename>).sign_file(<filename>, trusted_comment='<package_name> v<package_version>', drop_signature=True)` | Signs artifacts using [py-minisign](https://github.com/x13a/py-minisign). Note that the private key is stored as a [GitHub secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions). | | :white_check_mark: |
| Python Package Publishing | `uv publish` | Publish a python package to [PyPi](https://pypi.org/) using [uv](https://github.com/astral-sh/uv) based on settings in `pyproject.toml`. | | :white_check_mark: |

## Contributing Changes
Pull requests are preferred, since they are specific. For more about how to create a pull request, see https://help.github.com/articles/using-pull-requests/.

We recommend creating different branches for different (logical) changes, and creating a pull request into the `main` branch when you're done. For more information on creating branches, please see https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/.
