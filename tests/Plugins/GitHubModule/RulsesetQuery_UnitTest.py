# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for RulesetQuery.py"""

from RepoAuditor.Plugins.GitHub.RulesetQuery import RulesetQuery


def get_mock_request(
    status_code: int = 200,
):
    """A function which creates and returns a `mock_request` function."""

    class MockedResponse:
        def __init__(self, data, status_code):
            self._data = data
            self.status_code = status_code

        def json(self):
            return self._data

        @staticmethod
        def raise_for_status():
            pass

    def mock_request(method, url, *args, **kwargs):
        """The function to use for monkeypatching"""
        # remove leading /
        if len(url) > 0 and url[0] == "/":
            url = url[1:]

        if method.lower() == "get":
            if url == "":
                return MockedResponse({"default_branch": "main"}, status_code)
            elif url == "rules/branches/main":
                return MockedResponse(
                    [
                        {
                            "ruleset_id": 117,
                        },
                    ],
                    status_code,
                )
            elif url == "rulesets/117":
                return MockedResponse("valid-test-data", status_code)

    return mock_request


class TestRulesetQuery:
    def test_GetData(self, module_data, monkeypatch):
        """Test the GetData method."""
        monkeypatch.setattr(module_data["session"], "request", get_mock_request())
        query = RulesetQuery()
        query_data = query.GetData(module_data)

        assert len(query_data["rules"]) == 1
        assert query_data["rules"][0]["ruleset_id"] == 117
        assert query_data["rules"][0]["ruleset"] == "valid-test-data"
