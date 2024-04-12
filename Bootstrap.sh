#!/usr/bin/env bash
# ----------------------------------------------------------------------
# |
# |  This script downloads and invokes BootstrapImpl.sh from the PythonBootstrapper
# |  repository (https://github.com/davidbrownell/PythonBootstrapper).
# |
# |  Arguments:
# |
# |      --debug                         Display additional debugging information.
# |
# |      --force                         Ensure that a new python environment is installed, even if it already exists.
# |
# |      --python-version <version>      Specify the python version to install; the default python version is installed if not specified.
# |
# |      --bootstrap-branch <branch>     Specify the branch of the PythonBootstrapper repository to use when downloading BootstrapImpl; "main" is used if not specified.
# |
# ----------------------------------------------------------------------
set +v # Continue on errors

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd "${this_dir}" > /dev/null || exit

# ----------------------------------------------------------------------
# |
# |  Parse and Process Arguments
# |
# ----------------------------------------------------------------------
bootstrap_branch=main
command_line_args=()

while [[ $# -gt 0 ]]; do
    if [[ "$1" == "--bootstrap-branch" ]]; then
        bootstrap_branch=$2
        shift
    else
        command_line_args+=("$1")
    fi

    shift
done

# ----------------------------------------------------------------------
# |
# |  Download BootstrapImpl.sh
# |
# ----------------------------------------------------------------------
echo "Downloading Bootstrap code..."

bootstrap_url=https://raw.githubusercontent.com/davidbrownell/PythonBootstrapper/${bootstrap_branch}/src/BootstrapImpl.sh

temp_script_name=$(mktemp Bootstrap.XXXXXX)

curl --header "Cache-Control: no-cache, no-store" --header "Pragma: no-cache" --location ${bootstrap_url} --output BootstrapImpl.sh --no-progress-meter --fail-with-body > "${temp_script_name}" 2>&1
error=$?

if [[ ${error} != 0 ]]; then
    echo "[1ADownloading Bootstrap code...[31m[1mFAILED[0m (${bootstrap_url})."
    echo ""

    cat "${temp_script_name}"
    rm "${temp_script_name}"

    exit ${error}
fi

chmod u+x BootstrapImpl.sh
echo "[1ADownloading Bootstrap code...[32m[1mDONE[0m."

# ----------------------------------------------------------------------
# |
# |  Invoke BootstrapImpl.sh
# |
# ----------------------------------------------------------------------
./BootstrapImpl.sh "${command_line_args[@]}"
error=$?

# ----------------------------------------------------------------------
# |
# |  Exit
# |
# ----------------------------------------------------------------------
rm "BootstrapImpl.sh"
rm "${temp_script_name}"

exit ${error}
