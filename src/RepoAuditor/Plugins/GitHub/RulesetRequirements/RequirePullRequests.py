# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the RequirePullRequests object."""

import textwrap

from RepoAuditor.Plugins.GitHub.Impl.EnableRulesetRequirementImpl import EnableRulesetRequirementImpl


class RequirePullRequests(EnableRulesetRequirementImpl):
    """Require pull requests before merging to default branch."""

    def __init__(self) -> None:
        super().__init__(
            name="RequirePullRequestsRule",
            enabled_by_default=True,
            dynamic_arg_name="no",
            github_ruleset_type="pull_request",
            github_ruleset_value="Require a pull request before merging",
            get_configuration_value_func=self._GetValue,
            rationale=textwrap.dedent(
                """\
                The default behavior is to require pull requests before merging.
                This is because pull request reviews help maintain code quality.

                Reasons for this Default
                ------------------------
                - Pull requests are an important part of the development process and
                prevent unwanted changes from making it into the mainline branch.

                Reasons to Override this Default
                --------------------------------
                If this is a single contributor project and the developer is aware of
                the pros and cons of pushing directly to the primary development branch.
                """,
            ),
        )
