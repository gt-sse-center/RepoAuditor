# Personal Access Token (PAT)

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
10. Save the PAT to a convenient location on your machine (such as your home directory `~/`) in the file `PAT.txt`.

The path to the `PAT.txt` will be passed into `RepoAuditor`. E.g.

```sh
uvx RepoAuditor --GitHub-pat ~/PAT.txt
```
