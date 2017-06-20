import sys
import gdb
import adbg.modules.arch as arch
from types import ModuleType

class Reg():
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

class RegisterSet():
    def __init__(self, stack, pc):
        self._stack = stack
        self._pc = pc

    def readreg(self, name):
        value = gdb.selected_frame().read_register(name)
        return Reg(name, int(value))

    @property
    def stack(self):
        return self.readreg(self._stack)

    @property
    def pc(self):
        return self.readreg(self._pc)

arch_to_reg = {}
arch_to_reg['x86-64'] = RegisterSet(
        stack = 'rsp',
        pc = 'rip',
        )

class module(ModuleType):
    def __init__(self, name):
        self.name = name
        super(module, self).__init__(name)

    @property
    def stack(self):
        return arch_to_reg[arch.current].stack

    @property
    def pc(self):
        return arch_to_reg[arch.current].pc

sys.modules[__name__] = module(__name__)
