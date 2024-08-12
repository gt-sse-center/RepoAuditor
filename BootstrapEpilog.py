# pylint: disable=missing-module-docstring

import os
import subprocess
import sys

from pathlib import Path


# Parse the arguments
is_package = False
no_cache = False

display_flags: list[str] = []

# First arg is the script name, second arg is the name of the shell script to write to
for arg in sys.argv[2:]:
    if arg == "--package":
        is_package = True
        display_flags.append("package")
    elif arg == "--no-cache":
        no_cache = True
    else:
        sys.stderr.write(f"WARNING: '{arg}' is not a recognized argument.\n")

subprocess.run(
    'pip install --disable-pip-version-check {} --editable ".[dev{}]"'.format(
        "--no-cache-dir" if no_cache else "",
        ", package" if is_package else "",
    ),
    check=True,
    shell=True,
)

with (
    Path(__file__).parent / os.environ["PYTHON_BOOTSTRAPPER_GENERATED_DIR"] / "bootstrap_flags.json"
).open("w") as f:
    f.write("[{}]".format(", ".join(f'"{flag}"' for flag in display_flags)))
