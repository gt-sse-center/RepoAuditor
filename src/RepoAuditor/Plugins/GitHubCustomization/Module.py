# -------------------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# -------------------------------------------------------------------------------
"""Contains the GitHubCustomizationModule object"""

import os
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Any, Optional

import typer
from dbrownell_Common.TyperEx import TypeDefinitionItemType
from dbrownell_Common.Types import override

from RepoAuditor.Module import ExecutionStyle, Module

# from RepoAuditor.Module import RequiredArg

from .Query import CustomizationQuery


class GitHubCustomizationModule(Module):
    """Module that validates GitHub repository customization files."""

    def __init__(self) -> None:
        super(GitHubCustomizationModule, self).__init__(
            "GitHubCustomization",
            "Validates GitHub repository customization files.",
            ExecutionStyle.Parallel,
            [CustomizationQuery()],
            requires_explicit_include=False,  # Make this enabled by default
        )

    @override
    def GetDynamicArgDefinitions(self) -> dict[str, TypeDefinitionItemType]:
        return {
            "path": (
                str,
                typer.Option(
                    ".",
                    help="Path to the repository root directory. If not provided, will use URL from GitHub plugin.",
                ),
            ),
             "url": (
                str,
                typer.Option(
                    ".",
                    help="URL to the github repository.",
                ),
            ),
        }

    @override
    def GenerateInitialData(self, dynamic_args: dict[str, Any]) -> Optional[dict[str, Any]]:
        # Check if we have a path specified
        repo_path = dynamic_args.get("path", None)

        # If no path is specified, check if we can get the URL from GitHub plugin
        if repo_path is None or repo_path == ".":
            # Try to get URL from GitHub plugin
            github_url = dynamic_args.get("url", None)

            if github_url:
                # Create a temporary directory for cloning
                temp_dir = tempfile.mkdtemp(prefix="repo_auditor_")
                print(f"Cloning repository from {github_url} to {temp_dir}...")

                try:
                    # Clone the repository
                    result = subprocess.run(
                        ["git", "clone", "--depth", "1", github_url, temp_dir],
                        check=True,
                        capture_output=True,
                        text=True,
                    )

                    # Store the temp directory for cleanup later
                    dynamic_args["temp_dir"] = temp_dir
                    repo_path = temp_dir

                except subprocess.CalledProcessError as e:
                    print(f"Error cloning repository: {e.stderr}")
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                    return None
            else:
                # Use current directory as fallback
                repo_path = os.getcwd()

        # Make sure repo_path is a Path object
        if not isinstance(repo_path, Path):
            repo_path = Path(repo_path)

        # Verify that the path exists and is a directory
        if not repo_path.is_dir():
            print(f"Error: {repo_path} is not a directory")
            return None

        # Return a dictionary with the repo_path
        return {"repo_path": repo_path}

    @override
    def Cleanup(self, dynamic_args: dict[str, Any]) -> None:
        """Clean up any resources created during execution."""
        # Clean up temporary directory if one was created
        if "temp_dir" in dynamic_args:
            temp_dir = dynamic_args["temp_dir"]
            print(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)

        super(GitHubCustomizationModule, self).Cleanup(dynamic_args)
