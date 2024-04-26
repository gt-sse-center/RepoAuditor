# -------------------------------------------------------------------------------
# |                                                                             |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech  |
# |                     Distributed under the MIT License.                      |
# |                                                                             |
# -------------------------------------------------------------------------------
"""Executes one or more Modules"""

import sys

from typing import Any, Callable, Optional

from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common.InflectEx import inflect  # type: ignore[import-untyped]
from dbrownell_Common.Streams.Capabilities import Capabilities  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]
from rich.progress import Progress, TimeElapsedColumn

from .Module import EvaluateResult, ExecutionStyle, Module


# ----------------------------------------------------------------------
def Execute(
    dm: DoneManager,
    modules: list[Module],
    *,
    warnings_as_errors_module_names: Optional[set[str]] = None,
    ignore_warnings_module_names: Optional[set[str]] = None,
    max_num_threads: Optional[int] = None,
) -> None:
    warnings_as_errors_module_names = warnings_as_errors_module_names or set()
    ignore_warnings_module_names = ignore_warnings_module_names or set()

    with dm.Nested("Processing {}...".format(inflect.no("module", len(modules)))) as modules_dm:
        parallel: list[tuple[int, Module]] = []
        sequential: list[tuple[int, Module]] = []

        for index, module in enumerate(modules):
            if module.style == ExecutionStyle.Parallel:
                parallel.append((index, module))
            elif module.style == ExecutionStyle.Sequential:
                sequential.append((index, module))
            else:
                assert False, module.style  # pragma: no cover

        # Calculate the results

        # ----------------------------------------------------------------------
        def CreateStatusString(
            num_completed: int,  # pylint: disable=unused-argument
            num_success: int,
            num_error: int,
            num_warning: int,
            num_does_not_apply: int,
        ) -> str:
            return f"✅: {num_success} ❌: {num_error} ⚠️: {num_warning} 🚫: {num_does_not_apply}"

        # ----------------------------------------------------------------------
        def CalcResultInfo(
            module: Module,
            eval_infos: list[list[Module.EvaluateInfo]],
        ) -> tuple[int, str]:
            return_code = 0

            for eval_info_items in eval_infos:
                for eval_info in eval_info_items:
                    result = eval_info.result
                    if result == EvaluateResult.Warning:
                        if module.name in warnings_as_errors_module_names:
                            result = EvaluateResult.Error
                        elif module.name in ignore_warnings_module_names:
                            continue

                    if result == EvaluateResult.Error:
                        return -1, "errors were encountered"
                    elif result == EvaluateResult.Warning:
                        return_code = 1

            return return_code, "" if return_code == 0 else "warnings were encountered"

        # ----------------------------------------------------------------------

        results: list[Optional[list[list[Module.EvaluateInfo]]]] = [None] * len(modules)

        if parallel:
            # ----------------------------------------------------------------------
            def Prepare(
                context: Any,
                on_simple_status_func: Callable[[str], None],  # pylint: disable=unused-argument
            ) -> tuple[int, ExecuteTasks.TransformTasksExTypes.TransformFuncType]:
                module = context
                del context

                # ----------------------------------------------------------------------
                def Transform(
                    status: ExecuteTasks.Status,
                ) -> ExecuteTasks.TransformResultComplete:

                    # ----------------------------------------------------------------------
                    def OnStatus(num_completed: int, *args, **kwargs):
                        status.OnProgress(
                            num_completed, CreateStatusString(num_completed, *args, **kwargs)
                        )

                    # ----------------------------------------------------------------------

                    result: list[list[Module.EvaluateInfo]] = module.Evaluate(
                        OnStatus,
                        max_num_threads=max_num_threads,
                    )

                    result_code, result_status = CalcResultInfo(module, result)

                    return ExecuteTasks.TransformResultComplete(result, result_code, result_status)

                # ----------------------------------------------------------------------

                return module.GetNumRequirements(), Transform

            # ----------------------------------------------------------------------

            for (results_index, _), result in zip(
                parallel,
                ExecuteTasks.TransformTasksEx(
                    modules_dm,
                    "Processing parallel modules...",
                    [ExecuteTasks.TaskData(module.name, module) for _, module in parallel],
                    Prepare,
                    max_num_threads=max_num_threads,
                ),
            ):
                assert results[results_index] is None
                assert isinstance(result, list), result

                results[results_index] = result

        for index, (results_index, module) in enumerate(sequential):
            with modules_dm.Nested(
                "Processing '{}' ({} of {})...".format(
                    module.name,
                    index + 1 + len(parallel),
                    len(modules),
                ),
            ) as this_module_dm:
                with this_module_dm.YieldStdout() as stdout_context:
                    stdout_context.persist_content = False

                    # Technically speaking, it would be more correct to use `stdout_context.stream` here
                    # rather than referencing `sys.stdout` directly, but it is really hard to work with mocked
                    # stream as mocks will create mocks for everything called on the mock. Use sys.stdout
                    # directly to avoid that particular problem.
                    from unittest.mock import Mock, MagicMock

                    assert stdout_context.stream is sys.stdout or isinstance(
                        stdout_context.stream, (Mock, MagicMock)
                    ), stdout_context.stream

                    with Progress(
                        *Progress.get_default_columns(),
                        TimeElapsedColumn(),
                        "{task.fields[status]}",
                        console=Capabilities.Get(sys.stdout).CreateRichConsole(sys.stdout),
                        transient=True,
                        refresh_per_second=10,
                    ) as progress_bar:
                        progress_bar_task_id = progress_bar.add_task(
                            stdout_context.line_prefix,
                            status="",
                            total=module.GetNumRequirements(),
                            visible=True,
                        )

                        # ----------------------------------------------------------------------
                        def OnStatus(
                            num_completed: int,
                            num_success: int,
                            num_error: int,
                            num_warning: int,
                            num_does_not_apply: int,
                        ) -> None:
                            progress_bar.update(
                                progress_bar_task_id,
                                completed=num_completed,
                                status=CreateStatusString(
                                    num_completed,
                                    num_success,
                                    num_error,
                                    num_warning,
                                    num_does_not_apply,
                                ),
                            )

                        # ----------------------------------------------------------------------

                        this_results: list[list[Module.EvaluateInfo]] = module.Evaluate(
                            OnStatus,
                            max_num_threads=max_num_threads,
                        )

                        assert results[results_index] is None
                        results[results_index] = this_results

                        this_module_dm.result = CalcResultInfo(module, this_results)[0]
