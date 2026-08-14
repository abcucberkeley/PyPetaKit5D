"""
Shared helpers for the generated MCC wrapper functions.

Values crossing from Python into the compiled MATLAB binary pass through a
single encoding layer: MATLAB literal syntax. The parsers on the MATLAB side
reconstruct cell arrays and numeric arrays with eval()/str2num(), so any value
interpolated into such a literal has to be escaped as MATLAB source. Arguments
are handed to the process as an argv list rather than a shell command line, so
there is no second, shell-level quoting layer to get right.

This module is not intended to be used by end users.
"""
import subprocess


def matlab_str(value):
    """Format a value as a MATLAB single-quoted char literal.

    A literal single quote is escaped by doubling it, which is the escape the
    MATLAB parser expects inside a single-quoted char array. Only use this for
    values that reach eval()/str2num() on the MATLAB side; a plain char
    argument is passed through untouched and must not be doubled.
    """
    return "'" + str(value).replace("'", "''") + "'"


def matlab_cell(items):
    """Format an iterable as a MATLAB cell array literal of char arrays."""
    return "{" + ",".join(matlab_str(item) for item in items) + "}"


def matlab_array(items, separator=","):
    """Format an iterable as a MATLAB numeric array literal."""
    return "[" + separator.join(str(item) for item in items) + "]"


def matlab_logical_array(items):
    """Format an iterable as a MATLAB logical array literal."""
    return "[" + ",".join(str(item).lower() for item in items) + "]"


def _escape_for_launcher(token):
    """Escape a token against the shell expansion inside run_mccMaster.sh.

    The launcher does not exec its arguments directly. It re-wraps each one in
    double quotes and hands the result to eval:

        while [ $# -gt 0 ]; do token=$1; args="${args} \\"${token}\\""; shift; done
        eval "\\"${exe_dir}/mccMaster\\"" $args

    Inside those double quotes a backslash, dollar sign, backtick or double
    quote is still special, so a path containing one is corrupted before the
    binary ever sees it. Escaping them here survives that eval intact. This is
    a workaround for the launcher, not MATLAB syntax; see matlab_str for the
    separate MATLAB-level quoting.
    """
    for character in ("\\", '"', "$", "`"):
        token = token.replace(character, "\\" + character)
    return token


def run_mcc(cmdArgs, function_name):
    """Run the compiled MATLAB function and raise if it fails.

    cmdArgs is an argv list of the form
    [launcher, matlabRuntimeLoc, function_name, ...arguments]. The launcher
    consumes the runtime location itself and evals everything after it, so
    only that tail is escaped.

    stdout/stderr are inherited so MATLAB progress output continues to stream
    to the terminal while long jobs run.
    """
    launcher, matlabRuntimeLoc, *arguments = (str(arg) for arg in cmdArgs)
    argv = [launcher, matlabRuntimeLoc]
    argv += [_escape_for_launcher(argument) for argument in arguments]

    process = subprocess.run(argv)
    if process.returncode != 0:
        raise RuntimeError(
            f"{function_name} failed with exit code {process.returncode}. "
            f"See the MATLAB output above for details."
        )
    return process
