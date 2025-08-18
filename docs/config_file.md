# Configuration File

`RepoAuditor` accepts both a set of flags as well as a configuration YAML file.

The configuration (or config) file can make usage easier by recording preferences as well as facilitating sharing of enforced requirements within an organization.
We have provided a sample configuration file called [default_config.yaml](https://github.com/gt-sse-center/RepoAuditor/blob/main/default_config.yaml), which can be used as:

```sh
uvx RepoAuditor --config default_config.yaml
```

## Key Differences

There are some differences between the flags used in the CLI and the options provided in the config file.

### Multiple Values

For example, to include multiple module on the CLI, the user would use the `--include` multiple times.

```sh
uvx RepoAuditor --include CommunityStandards --include GitHub
```

However, since the config file accepts a list of values, the corresponding option is `includes` (which is plural).

```yaml
includes: ["GitHub", "CommunityStandards"]
```

This is similarly the case for `--exclude` on the CLI and `excludes` in the config file.

### Boolean Flags

On the CLI, the existence of a boolean flag, e.g. `--GitHub-Description-allow-empty` is sufficient to indicate that we want this setting to be enabled.

However since YAML files expect key-value pairs, in the config file, you will have to specify the same flag as:

```yaml
GitHub-Description-allow-empty: true
```

Similarly for the case where we wish to check a setting is turned off, we specify e.g. `--GitHub-no-MergeCommit` on the CLI, but in the config file, it would be

```yaml
GitHub-no-MergeCommit: true
```

Remember, to deactive a check, we have to add the `Module-Requirement` to the `excludes` list,

```yaml
excludes: ["GitHub-MergeCommit"]
```
