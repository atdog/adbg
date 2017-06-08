import sys
import gdb
from types import ModuleType

class module(ModuleType):
    @property
    def pid(self):
        i = gdb.selected_inferior()
        if i is not None:
            return i.pid
        return 0

sys.modules[__name__] = module(__name__, '')
