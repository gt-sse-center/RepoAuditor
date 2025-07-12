# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the PullRequestTemplate requirement."""

from RepoAuditor.Plugins.CommunityStandards.Impl.ExistsRequirementImpl import ExistsRequirementImpl


class PullRequestTemplate(ExistsRequirementImpl):
    """Validates that a pull request template is configured."""

    def __init__(self) -> None:
        super().__init__(
            "PullRequestTemplate",
            "PULL_REQUESTS_TEMPLATE",
            [
                ".github/PULL_REQUEST_TEMPLATE.md",
                "docs/PULL_REQUEST_TEMPLATE.md",
                "PULL_REQUEST_TEMPLATE.md",
                ".github/pull_request_template.md",
                "docs/pull_request_template.md",
                "pull_request_template.md",
                # Directory with multiple templates
                ".github/PULL_REQUEST_TEMPLATE",
            ],
            "Create a pull request template file in one of these locations: .github/PULL_REQUEST_TEMPLATE.md, .github/pull_request_template.md, docs/PULL_REQUEST_TEMPLATE.md, or PULL_REQUEST_TEMPLATE.md",
            "Pull request templates help standardize code contributions and expedite the review process by ensuring consistent PR format.",
        )
