# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
# pylint: disable=missing-module-docstring

import os
import subprocess
import sys

from pathlib import Path


# Parse the arguments
is_debug = False
is_force = False
is_verbose = False
is_package = False
no_cache = False

display_flags: list[str] = []

# First arg is the script name, second arg is the name of the shell script to write to
for arg in sys.argv[2:]:
    if arg == "--debug":
        is_debug = True
    elif arg == "--force":
        is_force = True
    elif arg == "--verbose":
        is_verbose = True
    elif arg == "--package":
        is_package = True
        display_flags.append("package")
    elif arg == "--no-cache":
        no_cache = True
    else:
        raise Exception("'{}' is not a recognized argument.".format(arg))

if is_debug:
    is_verbose = True

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
