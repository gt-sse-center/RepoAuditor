# Local Development

## Enlistment
Enlistment in this repository involves these steps.

<table>
<tr>
    <th>Step</th>
    <th>Command Line</th>
    <th>Description</th>
</tr>
<tr>
    <td>1. Clone the repository locally</td>
    <td><code>git clone https://github.com/gt-sse-center/RepoAuditor</code></td>
    <td><a href="https://git-scm.com/docs/git-clone" target="_blank">https://git-scm.com/docs/git-clone</a></td>
</tr>
<tr>
    <td>2. Bootstrap the environment</td>
    <td>
        <table>
            <tr>
                <th>Linux / MacOS</th>
                <td><code>./Bootstrap.sh [--python-version &lt;python version&gt;]</code></td>
            </tr>
            <tr>
                <th>Windows</th>
                <td><code>Bootstrap.cmd [--python-version &lt;python version&gt;]</code></td>
            </tr>
        </table>
    </td>
    <td>Prepares the repository for local development by enlisting in all dependencies.</td>
</tr>
<tr>
    <td>3. Activate the environment</td>
    <td>
        <table>
            <tr>
                <th>Linux / MacOS</th>
                <td><code>. ./Activate.sh</code></td>
            </tr>
            <tr>
                <th>Windows</th>
                <td><code>Activate.cmd</code></td>
            </tr>
        </table>
    </td>
    <td>
        <p>Activates the terminal for development. Each new terminal window must be activated.</p>
        <p>Activate.sh/.cmd is actually a shortcut to the most recently bootstrapped version of python (e.g. Activate3.11.sh/.cmd). With this functionality, it is possible to support multiple python versions in the same repository and activate each in a terminal using the python-specific activation script.</p>
    </td>
</tr>
<tr>
    <td>4. [Optional] Deactivate the environment</td>
    <td>
        <table>
            <tr>
                <th>Linux / MacOS</th>
                <td><code>. ./Deactivate.sh</code></td>
            </tr>
            <tr>
                <th>Windows</th>
                <td><code>Deactivate.cmd</code></td>
            </tr>
        </table>
    </td>
    <td>
        Deactivates the terminal environment. Deactivating is optional, as the terminal window itself may be closed when development activities are complete.
    </td>
</tr>
</table>

## Development Activities
Each of these activities can be invoked from an activated terminal on your local machine.

| Activity | Command Line | Description | Invoked by Continuous Integration |
| --- | --- | --- | :-: |
| Code Formatting | `python Build.py black [--format]` | Format source code using [black](https://github.com/psf/black) based on settings in `pyproject.toml`. | :white_check_mark: |
| Static Code Analysis | `python Build.py pylint` | Validate source code using [pylint](https://github.com/pylint-dev/pylint) based on settings in `pyproject.toml`. | :white_check_mark: |
| Automated Testing | `python Build.py pytest [--code-coverage]` | Run automated tests using [pytest](https://docs.pytest.org/) and (optionally) extract code coverage information using [coverage](https://coverage.readthedocs.io/) based on settings in `pyproject.toml`. | :white_check_mark: |
| Semantic Version Generation | `python Build.py update_version` | Generate a new [Semantic Version](https://semver.org) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored in `/src/RepoAuditor/__init__.py`. | :white_check_mark: |
| Python Package Creation | <p><code>python Build.py package</code></p><p>Requires that the repository was bootstrapped with the <code>--package</code> flag. | Create a python package using [setuptools](https://github.com/pypa/setuptools) based on settings in `pyproject.toml`. | :white_check_mark: |
| Python Package Publishing | <p><code>python Build.py publish</code></p><p>Requires that the repository was bootstrapped with the <code>--package</code> flag. | Publish a python package to [PyPi](https://pypi.org). | :white_check_mark: |
| Build Binaries | `python Build.py build_binaries` |  Create a python binary for your current operating system using [cx_Freeze](https://cx-freeze.readthedocs.io/) based on settings in `src/BuildBinary.py`. | :white_check_mark: |
| Development Docker Image | `python Build.py create_docker_image` | Create a [docker](https://docker.com) image for a bootstrapped development environment. This functionality is useful when adhering to the [FAIR principles for research software](https://doi.org/10.1038/s41597-022-01710-x) by supporting the creation of a development environment and its dependencies as they existed at the moment when the image was created. |  |
