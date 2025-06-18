# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Unit test for Executor.py"""

import sys
import textwrap
import time

from typing import cast

import pytest

from dbrownell_Common.Types import override
from dbrownell_Common.TestHelpers.StreamTestHelpers import (
    GenerateDoneManagerAndContent,
    InitializeStreamCapabilities,
)

from RepoAuditor.Display import *
from RepoAuditor.ExecuteModules import *
from RepoAuditor.Module import *
from RepoAuditor.Requirement import *


# ----------------------------------------------------------------------
pytest.fixture(InitializeStreamCapabilities(), scope="session", autouse=True)


# ----------------------------------------------------------------------
class MyModule(Module):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        *args,
        no_initial_data: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.no_initial_data = no_initial_data

    # ----------------------------------------------------------------------
    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {}

    # ----------------------------------------------------------------------
    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:
        assert not dynamic_args

        if self.no_initial_data:
            return None

        return {"module_name": self.name}

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _GetData(self) -> Optional[dict[str, Any]]:
        return {"module_name": self.name}


# ----------------------------------------------------------------------
class MyQuery(Query):
    # ----------------------------------------------------------------------
    @override
    def GetData(
        self,
        module_data: dict[str, Any],
        *args,
        **kwargs,
    ) -> Optional[dict[str, Any]]:
        if args or kwargs:
            super().__init__(*args, **kwargs)

        module_data["query_name"] = self.name
        return module_data


# ----------------------------------------------------------------------
class MyRequirement(Requirement):
    # ----------------------------------------------------------------------
    def __init__(self, result: EvaluateResult, *args) -> None:
        super().__init__(*args)

        self.result = result

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @override
    def _EvaluateImpl(
        self,
        query_data: dict[str, Any],
        requirement_args: dict[str, Any],
    ) -> Requirement.EvaluateImplResult:
        # Introduce a delay so that we can see things happening
        time.sleep(0.1)

        return Requirement.EvaluateImplResult(
            self.result,
            None,
            provide_resolution=True,
            provide_rationale=True,
        )


# ----------------------------------------------------------------------
class TestExecute:
    # ----------------------------------------------------------------------
    @pytest.mark.parametrize("single_threaded", [False, True])
    def test_Successful(self, single_threaded):
        modules: list[Module] = []

        # ----------------------------------------------------------------------
        def GetExecutionStyle(index: int) -> ExecutionStyle:
            return ExecutionStyle.Parallel if index % 2 == 0 else ExecutionStyle.Sequential

        # ----------------------------------------------------------------------

        for module_index in range(5):
            queries: list[Query] = []

            for query_index in range(4):
                requirements: list[Requirement] = []

                for requirement_index in range(5):
                    requirements.append(
                        MyRequirement(
                            EvaluateResult.Success,
                            f"Requirement-{module_index}-{query_index}-{requirement_index}",
                            "",
                            GetExecutionStyle(requirement_index),
                            "",
                            "",
                        ),
                    )

                queries.append(
                    MyQuery(
                        f"Query-{module_index}-{query_index}",
                        GetExecutionStyle(query_index),
                        requirements,
                    ),
                )

            modules.append(
                MyModule(
                    f"Module-{module_index}",
                    "",
                    GetExecutionStyle(module_index),
                    queries,
                ),
            )

        with DoneManager.Create(sys.stdout, "", line_prefix="") as dm:
            all_results = Execute(
                dm,
                [ModuleInfo(module, {}, {}) for module in modules],
                single_threaded=single_threaded,
            )

            assert dm.result == 0

            for results in all_results:
                assert all(result.result == EvaluateResult.Success for result in results)

    # ----------------------------------------------------------------------
    @pytest.mark.parametrize(
        "data",
        [
            (EvaluateResult.Error, -1, False, False),
            (EvaluateResult.Warning, 1, False, False),
            (EvaluateResult.Warning, -1, True, False),
            (EvaluateResult.Warning, 0, False, True),
            (EvaluateResult.DoesNotApply, 0, False, False),
        ],
    )
    def test_NotSuccess(self, data):
        test_result, expected_result, warnings_as_errors, ignore_warnings = data

        modules: list[Module] = []

        # ----------------------------------------------------------------------
        def GetExecutionStyle(index: int) -> ExecutionStyle:
            return ExecutionStyle.Parallel if index % 2 == 0 else ExecutionStyle.Sequential

        # ----------------------------------------------------------------------

        for module_index in range(2):
            queries: list[Query] = []

            for query_index in range(3):
                requirements: list[Requirement] = []

                for requirement_index in range(4):
                    requirements.append(
                        MyRequirement(
                            (test_result if requirement_index % 3 == 0 else EvaluateResult.Success),
                            f"Requirement-{module_index}-{query_index}-{requirement_index}",
                            "",
                            GetExecutionStyle(requirement_index),
                            "",
                            "",
                        ),
                    )

                queries.append(
                    MyQuery(
                        f"Query-{module_index}-{query_index}",
                        GetExecutionStyle(query_index),
                        requirements,
                    ),
                )

            modules.append(
                MyModule(
                    f"Module-{module_index}",
                    "",
                    GetExecutionStyle(module_index),
                    queries,
                ),
            )

        with DoneManager.Create(sys.stdout, "", line_prefix="") as dm:
            all_results = Execute(
                dm,
                [ModuleInfo(module, {}, {}) for module in modules],
                warnings_as_errors_module_names=(
                    set() if not warnings_as_errors else {module.name for module in modules}
                ),
                ignore_warnings_module_names=(
                    set() if not ignore_warnings else {module.name for module in modules}
                ),
            )

            assert dm.result == expected_result

            # Convert the results into a list of EvaluateResult values
            converted_results: list[EvaluateResult] = []

            for results in all_results:
                converted_results += [result.result for result in results]

            assert converted_results == [
                test_result,
                EvaluateResult.Success,
                EvaluateResult.Success,
                test_result,
                test_result,
                EvaluateResult.Success,
                EvaluateResult.Success,
                test_result,
                test_result,
                EvaluateResult.Success,
                EvaluateResult.Success,
                test_result,
                test_result,
                EvaluateResult.Success,
                EvaluateResult.Success,
                test_result,
                test_result,
                EvaluateResult.Success,
                EvaluateResult.Success,
                test_result,
                test_result,
                EvaluateResult.Success,
                EvaluateResult.Success,
                test_result,
            ]

    # ----------------------------------------------------------------------
    def test_NoModules(self):
        dm_and_content = GenerateDoneManagerAndContent()

        dm = cast(DoneManager, next(dm_and_content))

        all_results = Execute(dm, [])

        assert dm.result > 0, dm.result
        assert all_results == []

        assert cast(str, next(dm_and_content)) == textwrap.dedent(
            """\
            Heading...
              WARNING: There are no modules to process.
            DONE! (1, <scrubbed duration>)
            """,
        )

    # ----------------------------------------------------------------------
    def test_SingleParallel(self):
        dm_and_content = GenerateDoneManagerAndContent()

        all_results = Execute(
            cast(DoneManager, next(dm_and_content)),
            [ModuleInfo(MyModule("MyModule", "", ExecutionStyle.Parallel, []), {}, {})],
        )

        # No queries, so no results
        assert all_results == [[]]

    # ----------------------------------------------------------------------
    def test_NoInitialData(self):
        dm_and_content = GenerateDoneManagerAndContent()

        all_results = Execute(
            cast(DoneManager, next(dm_and_content)),
            [
                ModuleInfo(
                    MyModule("MyModule", "", ExecutionStyle.Sequential, [], no_initial_data=True),
                    {},
                    {},
                )
            ],
        )

        assert all_results == [[]]

        # Assuming major version is 3
        if sys.version_info[1] < 11:
            expected_content = textwrap.dedent(
                """\
            Heading...
              Processing 1 module...
                Processing 'MyModule' (1 of 1)...


                DONE! (ReturnCode.DOESNOTAPPLY, <scrubbed duration>)
              DONE! (ReturnCode.DOESNOTAPPLY, <scrubbed duration>)
            DONE! (ReturnCode.DOESNOTAPPLY, <scrubbed duration>)
            """,
            )
        else:
            # From version 3.11 onwards, IntEnum.__str__ returns the int value.
            expected_content = textwrap.dedent(
                """\
            Heading...
              Processing 1 module...
                Processing 'MyModule' (1 of 1)...


                DONE! (2, <scrubbed duration>)
              DONE! (2, <scrubbed duration>)
            DONE! (2, <scrubbed duration>)
            """,
            )

        assert cast(str, next(dm_and_content)) == expected_content


# ----------------------------------------------------------------------
class TestDisplayResults:
    # ----------------------------------------------------------------------
    @staticmethod
    @pytest.fixture
    def modules() -> list[MyModule]:
        return [
            MyModule(
                "Module1",
                "Module1 description",
                ExecutionStyle.Parallel,
                [
                    MyQuery(
                        "Query1",
                        ExecutionStyle.Parallel,
                        [
                            MyRequirement(
                                EvaluateResult.Success,
                                "Requirement1A",
                                "This is the description for Requirement1A",
                                ExecutionStyle.Parallel,
                                "resolution",
                                "rationale",
                            ),
                            MyRequirement(
                                EvaluateResult.Success,
                                "Requirement1B",
                                "This is the description for Requirement1B",
                                ExecutionStyle.Parallel,
                                "resolution",
                                "rationale",
                            ),
                        ],
                    ),
                ],
            ),
            MyModule(
                "Module2",
                "Module2 description",
                ExecutionStyle.Parallel,
                [
                    MyQuery(
                        "Query2",
                        ExecutionStyle.Parallel,
                        [
                            MyRequirement(
                                EvaluateResult.Success,
                                "Requirement2A",
                                "This is the description for Requirement2A",
                                ExecutionStyle.Parallel,
                                "resolution",
                                "rationale",
                            ),
                        ],
                    ),
                ],
            ),
        ]

    # ----------------------------------------------------------------------
    @pytest.mark.parametrize("display_rationale", [True, False])
    @pytest.mark.parametrize("display_resolution", [True, False])
    @pytest.mark.parametrize("verbose", [False, True])
    @pytest.mark.parametrize(
        "result",
        [
            EvaluateResult.Success,
            EvaluateResult.Warning,
            EvaluateResult.Error,
            EvaluateResult.DoesNotApply,
        ],
    )
    def test_Output(self, result, verbose, display_resolution, display_rationale, modules, capsys, snapshot):
        dm_and_content = GenerateDoneManagerAndContent(verbose=verbose)

        if result in [EvaluateResult.Warning, EvaluateResult.Error]:
            resolution = "resolution"
            rationale = "rationale"
        else:
            resolution = None
            rationale = None

        DisplayResults(
            cast(DoneManager, next(dm_and_content)),
            [
                [
                    Module.EvaluateInfo(
                        result,
                        "Context 1",
                        resolution,
                        rationale,
                        modules[0].queries[0].requirements[0],
                        modules[0].queries[0],
                        modules[0],
                    ),
                    Module.EvaluateInfo(
                        result,
                        "Context 2",
                        resolution,
                        rationale,
                        modules[0].queries[0].requirements[1],
                        modules[0].queries[0],
                        modules[0],
                    ),
                ],
                [
                    Module.EvaluateInfo(
                        result,
                        "Context 3",
                        resolution,
                        rationale,
                        modules[1].queries[0].requirements[0],
                        modules[1].queries[0],
                        modules[1],
                    ),
                ],
            ],
            display_resolution=display_resolution,
            display_rationale=display_rationale,
        )

        content = capsys.readouterr().out

        assert content == snapshot
