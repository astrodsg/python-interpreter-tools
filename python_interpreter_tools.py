import os
import sys


PY3 = sys.version[0] == "3"

if PY3:
    # bring back execfile and reload for interactive use
    def execfile(filepath,  globals=None, locals=None):
        if globals is None:
            globals = sys._getframe(1).f_globals
        if locals is None:
            locals = sys._getframe(1).f_locals
        with open(filepath, "r") as f:
            # import runpy
            # result = runpy.run_path(f,globals,locals)
            # globals.update(result) ??
            try:
                source = f.read()+"\n"
                fp = os.path.abspath(filepath)
                code = compile(source, fp, 'exec')
                exec(code, globals, locals)
            except KeyboardInterrupt:
                return


def dirquery(obj, pattern=None, case_sensitive=False):
    """
    take dir of an obj and search for matches based on pattern

    Parameters
    ----------
    pattern : string
    obj : python object
    case_sensitive : bool

    """
    if pattern is None:
        return dir(obj)

    import re
    flag = 0
    if case_sensitive:
        flag = 0
    else:
        flag = re.IGNORECASE

    # -----------------------
    matches = []
    for atr in dir(obj):
        rematch = re.search(pattern, atr, flag)
        if rematch is None:
            continue
        matches.append(atr)

    return matches


def fprint(func, max_lines=100, exclude_docstring=True, show=True):
    """ Prints out the source code (from file) for a function

    inspect.getsourcelines(func)

    """
    import inspect
    filepath = inspect.getsourcefile(func)
    code_lines, num = inspect.getsourcelines(func)

    # -----------------------
    to_print = []
    to_print.append("from: '{}'\n".format(filepath))
    to_print.append("line: {}\n\n".format(num))
    to_print += code_lines
    to_print = "".join(to_print[:max_lines])

    # -----------------------
    if exclude_docstring and func.__doc__ is not None and len(func.__doc__.rstrip()):
        msg = ' <for docstring see help({})> '.format(func.__name__)
        to_print = to_print.replace(func.__doc__, msg)

    if show:
        print(to_print)
    else:
        return to_print
