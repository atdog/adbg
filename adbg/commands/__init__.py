import gdb
import traceback
import functools

def GDBCommand(func, *a, **kw):
    class C(_Command):
        __doc__ = func.__doc__
        __name__ = func.__name__
    return C(func, *a, **kw)

class _Command(gdb.Command):
    def __init__(self, func):
        super(_Command, self).__init__ (func.__name__, gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION)
        self.function = func

    def split_args(self, argument):
        return gdb.string_to_argv(argument)

    def invoke(self, arg, from_tty):
        argv = self.split_args(arg)
        try:
            return self(*argv)
        except TypeError:
            print(traceback.format_exc())
            raise

    def __call__(self, *arg, **kwargs):
        try:
            return self.function(*arg, **kwargs)
        except TypeError as te:
            print(te)
            print('%r: %s' % (self.function.__name__.strip(),
                              self.function.__doc__.strip()))
        except Exception:
            print(traceback.format_exc())

class GDBCommandWithArgParser():
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, func):
        self.parser.prog = func.__name__

        @functools.wraps(func)
        def _ArgparsedCommand(*args):
            try:
                args = self.parser.parse_args(args)
            except SystemExit:
                # If passing '-h' or '--help', argparse attempts to kill the process.
                return
            return func(**vars(args))
        _ArgparsedCommand.__doc__ = self.parser.description

        return GDBCommand(_ArgparsedCommand)

import adbg.commands.context
import adbg.commands.attach
import adbg.commands.shellcmd
import adbg.commands.config
# import adbg.commands.test
