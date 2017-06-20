from adbg.commands import GDBCommand
import adbg.modules.memory as memory
import adbg.modules.color as color
import adbg.modules.arch as arch
from capstone import *

class CSArch():
    def __init__(self, cs_arch, cs_mode):
        self._arch = cs_arch
        self._mode = cs_mode

    @property
    def arch(self):
        return self._arch

    @property
    def mode(self):
        return self._mode

arch_constant = {}
arch_constant['x86-64'] = CSArch(CS_ARCH_X86, CS_MODE_64)


def disasm_pc(pc=None, line=10):
    if not pc:
        raise

    if type(pc) is str:
        pc = int(pc, 16)

    code = memory.read(pc, 8 * line).tobytes()
    csv = arch_constant[arch.current]

    md = Cs(csv.arch, csv.mode)

    result = []
    n = 0
    for i in md.disasm(code, pc):
        ins = "%s\t%s" % (i.mnemonic, i.op_str)
        if i.address == pc:
            line = "%s:\t%s" %(color.code_adr(hex(i.address)), color.code_val_pc(ins))
        else:
            line = "%s:\t%s" %(color.code_adr(hex(i.address)), ins)
        result.append(line)
        n += 1
        if n == line:
            break

    return result

@GDBCommand
def disasm(pc=None):
    if not pc:
        print("please specify the PC assress to disassemble")
        return

    result = disasm_pc(pc)

    while len(result) < 10:
        result.append('(bad)')

    n = 0
    for line in result:
        print(line)
        n += 1
        if n == line:
            break

