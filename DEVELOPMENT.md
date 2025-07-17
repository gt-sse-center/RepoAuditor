# DEVELOPMENT GUIDE

## Fork setup

| Step | Command Line | Additional Information |
| --- | --- | --- |
| 1. Fork the repository | -- | https://github.com/gt-sse-center/RepoAuditor/fork |
| 2. Create a PAT for your forked repository | -- | See [PAT setup instructions](README.md#personal-access-token-pat) |
| 3. Update your forked repository settings to match RepoAuditor's defaults | -- | -- |

## Local Development

### Enlistment

| Step | Command Line | Additional Information |
| --- | --- | --- |
| 1. Clone the repository locally. | `git clone https://github.com/gt-sse-center/RepoAuditor` | https://git-scm.com/docs/git-clone |
| 2. Install [uv](https://github.com/astral-sh/uv). | `curl -LsSf https://astral.sh/uv/install.sh \| sh` on macOS and Linux or <br/>`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` on Windows | https://docs.astral.sh |
| 3. Install dependencies. | `uv sync` | https://docs.astral.sh/uv/concepts/projects/sync |
| 4. Install [pre-commit](https://pre-commit.com/) hooks | `uv run pre-commit install` | https://pre-commit.com/#1-install-pre-commit |
| 5. If you wish to test against an enterprise server, add a remote named `enterprise` with the corresponding URL | E.g. `git remote add enterprise git@github.gatech.edu:sse-center/RepoAuditor.git` | |

### Setup

#### Basic Setup

Please follow these steps to allow for local testing.

- Fork the `RepoAuditor` repository. We will test against the fork since your generated PAT is applicable only for the fork.
- Create a PAT file as detailed in the [README](https://github.com/gt-sse-center/RepoAuditor/blob/main/README.md#personal-access-token-pat).
- Set your forked repository as the `origin` remote (this should already be the case but it's good to verify).

  ```sh
  git remote add origin git@github.com:<github-username>/RepoAuditor.git
  ```

- Update the URL in `default_config.yaml` to point to your fork.
- You should now be able to run the following and see valid output. There will be errors, which we will tackle next.

  ```sh
  uv run RepoAuditor --config default_config.yaml --GitHub-pat PAT.txt
  ```

#### Local Testing

You can now run local tests from the project root directory with

```sh
uv run pytest -k 'not EndToEndTest'
```

#### End-To-End Testing

To include tests against your `RepoAuditor` fork for comprehensive end-to-end testing, you can run:

```sh
uv run pytest
```

In order to run end-to-end tests, which make calls to the GitHub API, you need to configure your forked repository, else you will see a large number of test failures.

Please follow the steps below to complete the configuration.

- On the `General` settings page
  - Under `Features`
    - Check `Wikis`.
    - Check `Issues`.
    - Check `Projects`.
  - Under `Pull Requests`
    - With `Allow merge commits`, set the `Default commit message` to `Pull request title`.
    - Uncheck `Allow squash merging`.
    - Uncheck `Allow rebase merging`.
    - Check `Allow auto-merge`.
    - Check `Automatically delete head branches`.

- On the `Branches` settings page
  - Click `Add classic branch protection rule`.
  - Under `Branch name pattern`, type in `main`.
  - Check `Require a pull request before merging`.
  - Check `Require a pull request before merging -> Dismiss stale pull request approvals when new commits are pushed`.
  - Check `Require a pull request before merging -> Require approval of the most recent reviewable push`.
  - Check `Require status checks to pass before merging`, and add the `CI+CD Workflow / Validate (ubuntu-latest, 3.13)` or equivalent status check.
  - Check `Require conversation resolution before merging`.
  - Check `Require signed commits`.
  - Check `Do not allow bypassing the above settings`.

- On the `Advanced Security` settings page
  - Enable `Dependabot security updates`.

- Go to the `Actions` tab
  - Enable Workflows by clicking on `I understand my workflows, go ahead and enable them`.
  - Run the `CI+CD` workflow. You will be asked to enable it, please do so.
  - In the `Run workflow` dropdown to the right, click the `Run workflow` button. This should cause the action to run, don't worry if it fails, it is only needed for a check below.

- On the `Rules -> Rulesets` settings page, create a new branch ruleset called `Protect Main`:
  - Under `Target branches`, click `Add target -> Include by pattern` and type in `main`. Finalize by clicking `Add Inclusion pattern`.
  - Enable `Restrict deletions`
  - Enable `Require signed commits`
  - Enable `Require a pull request before merging` with 1 required approval.
  - Enable `Require status checks to pass` with the `CI+CD Workflow / Validate (ubuntu-latest, 3.12)` check.
  - Disable `Block force pushes`.
  - Be sure to hit `Save changes` at the end.

### Development Activities

| Activity | Command Line | Description | Used During Local Development | Invoked by Continuous Integration |
| --- | --- | --- | :-: | :-: |
| Code Formatting | `uv run ruff format` or<br>`uv run ruff format --check` | Format source code using [ruff](https://github.com/astral-sh/ruff) based on settings in `pyproject.toml`. | :white_check_mark: | :white_check_mark: (via [pre-commit](https://pre-commit.com/)) |
| Sort Imports | `uv run ruff check --fix --select I` | Sort imports in source files. | :white_check_mark: | |
| Static Code Analysis | `uv run ruff check` | Validate source code using [ruff](https://github.com/astral-sh/ruff) based on settings in `pyproject.toml`. | :white_check_mark: | :white_check_mark: (via [pre-commit](https://pre-commit.com/)) |
| Run pre-commit scripts | `uv run pre-commit run` | Run [pre-commit](https://pre-commit.com/) scripts based on settings in `.pre-commit-config.yaml`. | :white_check_mark: | :white_check_mark: |
| Automated Testing | `uv run pytest` or<br/>`uv run pytest --no-cov` | Run automated tests using [pytest](https://docs.pytest.org/) and extract code coverage using [coverage](https://coverage.readthedocs.io/) based on settings in `pyproject.toml`. | :white_check_mark: | :white_check_mark: |
| Semantic Version Generation | `uv run python -m AutoGitSemVer.scripts.UpdatePythonVersion ./src/RepoAuditor/__init__.py ./src` | Generate a new [Semantic Version](https://semver.org/) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored in `./src/RepoAuditor/__init__.py`. | | :white_check_mark: |
| Python Package Creation | `uv build` | Create a python package using [uv](https://github.com/astral-sh/uv) based on settings in `pyproject.toml`. Generated packages will be written to `./dist`. | | :white_check_mark: |
| Sign Artifacts | `uv run --with py-minisign python -c "import minisign; minisign.SecretKey.from_file(<temp_filename>).sign_file(<filename>, trusted_comment='<package_name> v<package_version>', drop_signature=True)` | Signs artifacts using [py-minisign](https://github.com/x13a/py-minisign). Note that the private key is stored as a [GitHub secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions). | | :white_check_mark: |
| Python Package Publishing | `uv publish` | Publish a python package to [PyPi](https://pypi.org/) using [uv](https://github.com/astral-sh/uv) based on settings in `pyproject.toml`. | | :white_check_mark: |

### Contributing Changes

Pull requests are preferred, since they are specific. For more about how to create a pull request, see [this guide](https://help.github.com/articles/using-pull-requests/).

We recommend creating different branches for different (logical) changes, and creating a pull request into the `main` branch when you're done. For more information on creating branches, please see [this GitHub guide](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/).

### Verifying Signed Artifacts

Artifacts are signed and validated using [py-minisign](https://github.com/x13a/py-minisign) and the public key in the file `./minisign_key.pub`.

To verify that an artifact is valid, visit [the latest release](https://github.com/gt-sse-center/RepoAuditor/releases/latest) and download the `.minisign` signature file that corresponds to the artifact, then run the following command, replacing `<filename>` with the name of the artifact to be verified:

```shell
uv run --with py-minisign python -c "import minisign; minisign.PublicKey.from_file('minisign_key.pub').verify_file('<filename>')"
```
