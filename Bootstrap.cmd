@REM ----------------------------------------------------------------------
@REM |
@REM |  This script downloads and invokes BoostrapImpl.cmd from the PythonBootstrapper
@REM |  repository (https://github.com/davidbrownell/PythonBootstrapper).
@REM |
@REM |  Arguments:
@REM |
@REM |      --debug                         Display additional debugging information.
@REM |
@REM |      --force                         Ensure that a new python environment is installed, even if it already exists.
@REM |
@REM |      --python-version <version>      Specify the python version to install; the default python version is installed if not specified.
@REM |
@REM |      --bootstrap-branch <branch>     Specify the branch of the PythonBootstrapper repository to use when downloading BootstrapImpl; "main" is used if not specified.
@REM |
@REM ----------------------------------------------------------------------
@setlocal EnableDelayedExpansion
@pushd %~dp0

@REM ----------------------------------------------------------------------
@REM |
@REM |  Parse and Process Arguments
@REM |
@REM ----------------------------------------------------------------------
@set _BOOTSTRAP_BRANCH=main
@set _COMMAND_LINE_ARGS=

:ParseArgs
@if '%1' EQU '' @goto :ParseArgs_End

@set ARG=%1
@set ARG=%ARG:"=%

@if "%ARG%" NEQ "--bootstrap-branch" @goto :ParseArgs_BootstrapBranchEnd

@REM Extract the bootstrap branch
@shift /1

@set ARG=%1
@set ARG=%ARG:"=%

@set _BOOTSTRAP_BRANCH=%ARG%
@goto :ParseArgs_Next

:ParseArgs_BootstrapBranchEnd
@set _COMMAND_LINE_ARGS=%_COMMAND_LINE_ARGS% %1

:ParseArgs_Next
@shift /1
@goto :ParseArgs

:ParseArgs_End

@REM ----------------------------------------------------------------------
@REM |
@REM |  Download BootstrapImpl.cmd
@REM |
@REM ----------------------------------------------------------------------
@echo Downloading Bootstrap code...

@set _BOOTSTRAPIMPL_URL=https://raw.githubusercontent.com/davidbrownell/PythonBootstrapper/%_BOOTSTRAP_BRANCH%/src/BootstrapImpl.cmd

@call :_CreateTempFileName

@curl --header "Cache-Control: no-cache, no-store" --header "Pragma: no-cache" --location %_BOOTSTRAPIMPL_URL% --output BootstrapImpl.cmd --no-progress-meter --fail-with-body > "%_BOOTSTRAP_TEMP_FILENAME%" 2>&1
@set _ERRORLEVEL=%ERRORLEVEL%

@if %_ERRORLEVEL% NEQ 0 (
    @echo [1ADownloading Bootstrap code...[31m[1mFAILED[0m ^(%_BOOTSTRAPIMPL_URL%^).
    @echo.

    @type "%_BOOTSTRAP_TEMP_FILENAME%"
    @goto :Exit
)

@call :_DeleteTempFile
@echo [1ADownloading Bootstrap code...[32m[1mDONE[0m.

@REM ----------------------------------------------------------------------
@REM |
@REM |  Invoke BootstrapImpl.cmd
@REM |
@REM ----------------------------------------------------------------------
@call BootstrapImpl.cmd %_COMMAND_LINE_ARGS%
@set _ERRORLEVEL=%ERRORLEVEL%

@REM ----------------------------------------------------------------------
@REM |
@REM |  Exit
@REM |
@REM ----------------------------------------------------------------------
:Exit
@if exist BootstrapImpl.cmd del BootstrapImpl.cmd
@call :_DeleteTempFile

@popd

@endlocal & @exit /B %_ERRORLEVEL%

@REM ----------------------------------------------------------------------
@REM ----------------------------------------------------------------------
@REM ----------------------------------------------------------------------
:_CreateTempFileName
@set _BOOTSTRAP_TEMP_FILENAME=%CD%\Bootstrap-!RANDOM!-!Time:~6,5!
@goto :EOF

@REM ----------------------------------------------------------------------
:_DeleteTempFile
@if "%_BOOTSTRAP_TEMP_FILENAME%" NEQ "" (
    @if exist "%_BOOTSTRAP_TEMP_FILENAME%" (
        @del "%_BOOTSTRAP_TEMP_FILENAME%"
    )
)
@goto :EOF
