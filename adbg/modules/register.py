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
    def __init__(self,
            stack,
            pc,
            frame=None,
            flags=dict(),
            gpr=tuple(),
            misc=tuple(),
            retval=None):

        self._stack = stack
        self._pc = pc
        self._frame = frame
        self._flags = flags
        self._gpr = gpr
        self._misc = misc
        self._retval = retval

        self.common = []
        for reg in gpr + (frame, stack, pc):
            if reg and reg not in self.common:
                self.common.append(reg)
        self.all = set(i for i in misc) | set(flags) | set(self.common)
        self.all -= {None}

    def __iter__(self):
        for r in self.common:
            yield self.readreg(r)

    def readreg(self, name):
        value = gdb.selected_frame().read_register(name)
        return Reg(name, int(value))

    @property
    def stack(self):
        return self.readreg(self._stack)

    @property
    def pc(self):
        return self.readreg(self._pc)

x86flags = {'eflags': {
    'CF':  0,
    'PF':  2,
    'AF':  4,
    'ZF':  6,
    'SF':  7,
    'IF':  9,
    'DF': 10,
    'OF': 11,
}}

amd64 = RegisterSet(pc      = 'rip',
                    stack   = 'rsp',
                    frame   = 'rbp',
                    flags   = x86flags,
                    gpr     = ('rax','rbx','rcx','rdx','rdi','rsi',
                               'r8', 'r9', 'r10','r11','r12',
                               'r13','r14','r15'),
                    misc    =  ('cs','ss','ds','es','fs','gs',
                                'fsbase', 'gsbase',
                                'ax','ah','al',
                                'bx','bh','bl',
                                'cx','ch','cl',
                                'dx','dh','dl',
                                'dil','sil','spl','bpl',
                                'di','si','bp','sp','ip'),
                    retval  = 'rax')

i386 = RegisterSet( pc      = 'eip',
                    stack   = 'esp',
                    frame   = 'ebp',
                    flags   = x86flags,
                    gpr     = ('eax','ebx','ecx','edx','edi','esi'),
                    misc    =  ('cs','ss','ds','es','fs','gs',
                                'fsbase', 'gsbase',
                                'ax','ah','al',
                                'bx','bh','bl',
                                'cx','ch','cl',
                                'dx','dh','dl',
                                'dil','sil','spl','bpl',
                                'di','si','bp','sp','ip'),
                    retval  = 'eax')

arch_to_reg = {}
arch_to_reg['x86-64'] = amd64
arch_to_reg['i386'] = i386

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

    def __iter__(self):
        return arch_to_reg[arch.current].__iter__()

sys.modules[__name__] = module(__name__)
