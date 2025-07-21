# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains functionality to display the results of executing modules."""

import textwrap
from typing import Optional

from dbrownell_Common import TextwrapEx  # type: ignore[import-untyped]
from dbrownell_Common.Streams.DoneManager import DoneManager  # type: ignore[import-untyped]
from rich import print as rich_print
from rich.console import Group
from rich.panel import Panel

from RepoAuditor.Module import EvaluateResult, Module


def GetInternalPanelContent(
    dm: DoneManager,
    results: list[Module.EvaluateInfo],
    display_resolution: bool,  # noqa: FBT001
    display_rationale: bool,  # noqa: FBT001
    num_success: int,
    num_warning: int,
    num_error: int,
    num_does_not_apply: int,
    num_requirements: int,
) -> list[Panel | str]:
    """Get the content for each result to be displayed inside the internal panel."""
    internal_content: list[Panel | str] = []

    module = results[0].module

    if module.description:
        internal_content.append(f"{module.description.strip()}\n")

    metrics_display = textwrap.dedent(
        f"""\
            [grey66]
            Successful:     {num_success} ({(num_success / num_requirements):.02%})
            Warnings:       {num_warning} ({(num_warning / num_requirements):.02%})
            Errors:         {num_error} ({(num_error / num_requirements):.02%})
            Skipped:        {num_does_not_apply} ({(num_does_not_apply / num_requirements):.02%})
        """,
    )
    internal_content.append(metrics_display)

    for result in results:
        if not dm.is_verbose and result.result in [
            EvaluateResult.Success,
            EvaluateResult.DoesNotApply,
        ]:
            continue

        if result.result == EvaluateResult.Success:
            border_color = "green"
        elif result.result == EvaluateResult.Warning:
            border_color = "yellow"
        elif result.result == EvaluateResult.Error:
            border_color = "red"
        elif result.result == EvaluateResult.DoesNotApply:
            border_color = ""
        else:
            raise RuntimeError(result.result)  # pragma: no cover

        content: list[str] = []

        if result.requirement.description:
            content.append(f"{result.requirement.description.strip()}\n")

        if result.context:
            content.append(f"{result.result.name.upper()}: {result.context.strip()}\n")

        if display_resolution and result.resolution:
            content.append(
                textwrap.dedent(
                    """\
                        Resolution
                        ----------
                          {}
                        """,
                ).format(TextwrapEx.Indent(result.resolution.strip(), 2, skip_first_line=True)),
            )

        if display_rationale and result.rationale:
            content.append(
                textwrap.dedent(
                    """\
                        Rationale
                        ---------
                          {}
                        """,
                ).format(TextwrapEx.Indent(result.rationale.strip(), 2, skip_first_line=True)),
            )

        internal_content.append(
            Panel(
                Group(*content),
                title=f"[{result.result.name}] {result.requirement.name}",
                title_align="left",
                border_style=border_color,
                padding=(1, 1, 0, 1) if content else 0,
            ),
        )

    # Finally print statistics at the end in a panel if verbose
    internal_content.append(
        Panel(
            metrics_display,
            title="Metrics",
            title_align="left",
            border_style="grey66",
            padding=(1, 1, 0, 1),
        ),
    )

    return internal_content


# ----------------------------------------------------------------------
def DisplayResults(
    dm: DoneManager,
    all_results: list[list[Module.EvaluateInfo]],
    *,
    display_resolution: bool,
    display_rationale: bool,
    panel_width: Optional[int] = None,
) -> None:
    """Display the results of executing the modules."""
    for results in all_results:
        assert results
        module = results[0].module

        num_success = 0
        num_warning = 0
        num_error = 0
        num_does_not_apply = 0

        for result in results:
            if result.result == EvaluateResult.Success:
                num_success += 1
            elif result.result == EvaluateResult.Warning:
                num_warning += 1
            elif result.result == EvaluateResult.Error:
                num_error += 1
            elif result.result == EvaluateResult.DoesNotApply:
                num_does_not_apply += 1
            else:
                raise RuntimeError(result.result)  # pragma: no cover

        num_requirements = module.GetNumRequirements()
        assert num_requirements

        internal_content: list[Panel | str] = GetInternalPanelContent(
            dm,
            results,
            display_resolution,
            display_rationale,
            num_success=num_success,
            num_warning=num_warning,
            num_error=num_error,
            num_does_not_apply=num_does_not_apply,
            num_requirements=num_requirements,
        )

        rich_print(
            Panel(
                Group(*internal_content),
                padding=1 if internal_content else 0,
                title=results[0].module.name,
                width=panel_width,
            ),
        )
