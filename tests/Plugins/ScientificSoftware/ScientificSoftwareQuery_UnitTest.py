# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for ScientificSoftwareQuery.py"""

from RepoAuditor.Plugins.ScientificSoftware.ScientificSoftwareQuery import ScientificSoftwareQuery
from CommunityStandards.CommunityStandardsQuery_UnitTest import TestCommunityStandardsQuery


class TestScientificSoftwareQuery(TestCommunityStandardsQuery):
    """Tests for ScientificSoftwareQuery class."""

    query = ScientificSoftwareQuery()
