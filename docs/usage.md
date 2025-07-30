# Usage

With a generated PAT file, you can now run `RepoAuditor` on your GitHub repository.

As a general example, we will use the [python-helloworld](https://github.com/dbarnett/python-helloworld) repository.

> **NOTE** You need to fork the repository since your default PAT only has access to repos under your account.

To run `RepoAuditor`, we can enter the following in the command-line:

```shell
uvx RepoAuditor --include GitHub \
  --GitHub-url https://github.com/<username>/python-helloworld \
  --GitHub-pat ~/PAT.txt
```

`RepoAuditor` will generate a series of messages describing all the issues in the repository, along with the rationale behind them and the steps for resolution.

<br/>

## Custom Settings

`RepoAuditor` tries to provide default settings and checks which are considered best practices. However, your team or organization may have different ways of doing things.
You can override the default settings by specifying the appropriate flag.

We have 3 types of flags:

1. Boolean flags for those settings which are checked to be on by default and you wish to check are off, with the form `Module-no-Requirement` (e.g. `--GitHub-no-MergeCommit`).
2. Conversely, boolean flags for those settings which are checked to be off by default, and you wish to check are on, denoted by the form `Module-Requirement` (e.g. `--GitHub-AllowDeletions`).
3. Values flags take a string value to determine what value to enforce, and have the form `Module-Requirement-value` (e.g. `--GitHub-License-value "MIT License"`).

Please run `uvx repoauditor --help` to get the list of all flags available.

<br/>

## Examples

For example, `RepoAuditor` by default checks that the setting `Allow rebase merging` is off. If you wish to check that this setting is turned on, you can run:

```shell
uvx repoauditor --GitHub-RebaseMergeCommit
```

Similarly, `RepoAuditor` checks if `Issues` are enabled. You can set `RepoAuditor` to check if `Issues` is disabled by specifying

```shell
uvx repoauditor --GitHub-no-SupportIssues
```

Finally, `RepoAuditor` by default enforces that the `MIT License` exists for the repository. If your organization requires another license (such as `GPL`), you can enforce that by specifying the license keyword such as:

```shell
uvx repoauditor --GitHub-License-value "GNU General Public License v2.0"
```

The types of licenses supported by GitHub can be found [here](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#searching-github-by-license-type). Be sure to specify the full license name, e.g. `GNU General Public License v2.0`.
