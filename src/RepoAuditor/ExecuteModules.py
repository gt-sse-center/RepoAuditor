# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains functionality to execute multiple Modules."""

import itertools
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional, cast

from dbrownell_Common import ExecuteTasks  # type: ignore[import-untyped]
from dbrownell_Common.InflectEx import inflect  # type: ignore[import-untyped]
from dbrownell_Common.Streams.Capabilities import Capabilities  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]
from rich.progress import Progress, TimeElapsedColumn

from RepoAuditor.Module import EvaluateResult, ExecutionStyle, Module, OnStatusFunc
from RepoAuditor.Requirement import ReturnCode


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ModuleInfo:
    """Information about a Module."""

    module: Module
    dynamic_args: dict[str, Any]
    requirement_args: dict[str, Any]


# ----------------------------------------------------------------------
# |
# |  Public Functions
# |
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
def Evaluate(
    module_info: ModuleInfo,
    on_status_func: OnStatusFunc,
    max_num_threads: Optional[int],
) -> list[list[Module.EvaluateInfo]]:
    """Evaluate the module given the dynamic arguments.

    Returns a list of information pertaining to module evaluation,
    with it subgrouped as lists themselves, hence a list of lists.
    """
    module_data = module_info.module.GenerateInitialData(module_info.dynamic_args)
    if module_data is None:
        return []

    return module_info.module.Evaluate(
        module_data,
        module_info.requirement_args,
        on_status_func,
        max_num_threads=max_num_threads,
    )


# ----------------------------------------------------------------------
def CalcResultInfo(
    all_eval_infos: list[list[Module.EvaluateInfo]],
    warnings_as_errors_module_names: set[str],
    ignore_warnings_module_names: set[str],
) -> tuple[int, str]:
    """Calculate the result of evaluating the modules as given in `all_eval_infos`.

    Returns a code value indicating success, warning, or error,
    as well as a string description of the result.
    If the result is a warning or error, return immediately.
    "Does Not Apply" is considered as a success.
    """
    return_code = ReturnCode.SUCCESS
    return_msg = ""

    if not all_eval_infos:
        return ReturnCode.DOESNOTAPPLY, "module does not apply"

    for eval_infos in all_eval_infos:
        for eval_info in eval_infos:
            result = eval_info.result

            if result == EvaluateResult.Warning:
                if eval_info.module.name in warnings_as_errors_module_names:
                    # Treat warnings as errors enabled so recast the result type
                    result = EvaluateResult.Error
                elif eval_info.module.name in ignore_warnings_module_names:
                    continue

            if result == EvaluateResult.Error:
                return ReturnCode.ERROR, "errors were encountered"

            if result == EvaluateResult.Warning:
                return_code, return_msg = ReturnCode.WARNING, "warnings were encountered"

    return return_code, return_msg


def Execute(
    dm: DoneManager,
    module_infos: list[ModuleInfo],
    warnings_as_errors_module_names: Optional[set[str]] = None,
    ignore_warnings_module_names: Optional[set[str]] = None,
    *,
    single_threaded: bool = False,
) -> list[list[Module.EvaluateInfo]]:
    """Execute the modules in parallel and/or sequentially."""
    if not module_infos:
        dm.WriteWarning("There are no modules to process.\n")
        return []

    warnings_as_errors_module_names = warnings_as_errors_module_names or set()
    ignore_warnings_module_names = ignore_warnings_module_names or set()
    max_num_threads = 1 if single_threaded else None

    with dm.Nested("Processing {}...".format(inflect.no("module", len(module_infos)))) as modules_dm:
        # Organize the modules into those that can be run in parallel and those that must be run
        # sequentially.
        parallel: list[tuple[int, ModuleInfo]] = []
        sequential: list[tuple[int, ModuleInfo]] = []

        for index, module_info in enumerate(module_infos):
            if module_info.module.style == ExecutionStyle.Parallel:
                parallel.append((index, module_info))
            elif module_info.module.style == ExecutionStyle.Sequential:
                sequential.append((index, module_info))
            else:
                raise RuntimeError(module_info.module.style)  # pragma: no cover

        if len(parallel) == 1:
            sequential.append(parallel[0])
            parallel = []

        # Calculate the results
        # ----------------------------------------------------------------------
        all_results: list[Optional[list[list[Module.EvaluateInfo]]]] = [None] * len(module_infos)

        if parallel:
            # ----------------------------------------------------------------------
            def Prepare(
                context: Any,  # noqa: ANN401
                on_simple_status_func: Callable[[str], None],  # noqa: ARG001
            ) -> tuple[int, ExecuteTasks.TransformTasksExTypes.TransformFuncType]:
                module_info = cast(ModuleInfo, context)
                del context

                # ----------------------------------------------------------------------
                def Transform(
                    status: ExecuteTasks.Status,
                ) -> ExecuteTasks.CompleteTransformResult:
                    # ----------------------------------------------------------------------
                    def OnStatus(num_completed: int, *args, **kwargs) -> None:
                        status.OnProgress(
                            num_completed,
                            _CreateStatusString(*args, **kwargs),
                        )

                    # ----------------------------------------------------------------------

                    evaluate_results = Evaluate(module_info, OnStatus, max_num_threads=max_num_threads)

                    result_code, result_status = CalcResultInfo(
                        evaluate_results,
                        warnings_as_errors_module_names=warnings_as_errors_module_names,
                        ignore_warnings_module_names=ignore_warnings_module_names,
                    )

                    return ExecuteTasks.CompleteTransformResult(evaluate_results, result_code, result_status)

                # ----------------------------------------------------------------------

                return module_info.module.GetNumRequirements(), Transform

            # ----------------------------------------------------------------------

            for (all_results_index, _), transformed_results in zip(
                parallel,
                ExecuteTasks.TransformTasksEx(
                    modules_dm,
                    "Processing parallel modules...",
                    [
                        ExecuteTasks.TaskData(module_info.module.name, module_info)
                        for _, module_info in parallel
                    ],
                    Prepare,
                    max_num_threads=max_num_threads,
                ),
                strict=True,
            ):
                assert all_results[all_results_index] is None
                assert isinstance(transformed_results, list), transformed_results

                all_results[all_results_index] = transformed_results

        for index, (all_results_index, module_info) in enumerate(sequential):
            with (
                modules_dm.Nested(
                    f"Processing '{module_info.module.name}' ({index + 1 + len(parallel)} of {len(module_infos)})...",
                ) as this_module_dm,
                # rich.progress needs to output to sys.stdout
                this_module_dm.YieldStdout() as stdout_context,
            ):
                stdout_context.persist_content = False

                # Technically speaking, it would be more correct to use `stdout_context.stream` here
                # rather than referencing `sys.stdout` directly, but it is really hard to work with mocked
                # stream as mocks will create mocks for everything called on the mock. Use sys.stdout
                # directly to avoid that particular problem.
                from unittest.mock import MagicMock, Mock

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
                        total=module_info.module.GetNumRequirements(),
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
                            progress_bar_task_id,  # noqa: B023
                            completed=num_completed,
                            status=_CreateStatusString(
                                num_success,
                                num_error,
                                num_warning,
                                num_does_not_apply,
                            ),
                        )

                    # ----------------------------------------------------------------------

                    evaluate_results = Evaluate(module_info, OnStatus, max_num_threads=max_num_threads)

                    assert all_results[all_results_index] is None
                    all_results[all_results_index] = evaluate_results

                    this_module_dm.result = CalcResultInfo(
                        evaluate_results,
                        warnings_as_errors_module_names=warnings_as_errors_module_names,
                        ignore_warnings_module_names=ignore_warnings_module_names,
                    )[0]

    final_results: list[list[Module.EvaluateInfo]] = []

    for results in all_results:
        if results is None:
            continue  # pragma: no cover

        final_results.append(list(itertools.chain(*results)))

    return final_results


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _CreateStatusString(
    num_success: int,
    num_error: int,
    num_warning: int,
    num_does_not_apply: int,
) -> str:
    return f"✅: {num_success} ❌: {num_error} ⚠️: {num_warning} 🚫: {num_does_not_apply}"
