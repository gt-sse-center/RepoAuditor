# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit tests for ClassicBranchProtectionQuery.py"""

from RepoAuditor.Plugins.GitHub.ClassicBranchProtectionQuery import ClassicBranchProtectionQuery


def get_mock_request(
    status_code: int = 200,
    protected_branch: bool = True,
    rulesets_exist: bool = True,
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
            elif url == "branches/main":
                return MockedResponse({"protected": protected_branch}, status_code)
            elif url == "branches/main/protection":
                return MockedResponse("valid-test-data", status_code)
            elif url == "rules/branches/main":
                if rulesets_exist:
                    return MockedResponse("valid-rules", status_code=200)
                else:
                    return MockedResponse("", status_code=200)

    return mock_request


class TestClassicBranchProtectionQuery:
    def test_GetData(self, module_data, monkeypatch):
        """Test successful GetData"""
        monkeypatch.setattr(module_data["session"], "request", get_mock_request())
        query = ClassicBranchProtectionQuery()
        query_data = query.GetData(module_data)

        assert query_data["branch_protection_data"] == "valid-test-data"

    def test_NotProtected(self, module_data, monkeypatch):
        """Test where branch is not protected."""
        monkeypatch.setattr(module_data["session"], "request", get_mock_request(protected_branch=False))
        query = ClassicBranchProtectionQuery()
        query_data = query.GetData(module_data)

        assert query_data is None

    def test_RulesetProtected(self, module_data, monkeypatch):
        """Test when the branch is protected by rulesets."""
        monkeypatch.setattr(module_data["session"], "request", get_mock_request(status_code=404))
        query = ClassicBranchProtectionQuery()
        query_data = query.GetData(module_data)

        assert query_data is None

    def test_RulesetProtectedNoRules(self, module_data, monkeypatch):
        """Test when the branch is protected by rulesets, but no rules exist."""
        monkeypatch.setattr(
            module_data["session"], "request", get_mock_request(status_code=404, rulesets_exist=False)
        )
        # Set github_pat to None to test a pathway
        module_data["session"].github_pat = None
        query = ClassicBranchProtectionQuery()
        query_data = query.GetData(module_data)

        assert query_data is None
