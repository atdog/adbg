import sys
import struct
import gdb
import adbg
import adbg.modules.config as config
import adbg.modules.register as register
import adbg.modules.memory as memory
import adbg.modules.color as color
import adbg.modules.arch as arch
from adbg.commands.disasm import disasm_pc
from adbg.commands import GDBCommand

config.boolean('context', 'reg', "on")
config.int('context', 'reg_w', "4")

config.boolean('context', 'code', "on")
config.int('context', 'code_s', "10")

config.boolean('context', 'stack', "on")
config.int('context', 'stack_w', "5")
config.int('context', 'stack_h', "5")


@GDBCommand
def reg():
    print(color.banner('reg'))

    if arch.endian == 'little':
        endian = ">"
    else:
        endian = "<"

    i = 0
    for r in register:
        if i % config.context.reg_w == 0 and i != 0:
            print()
        if arch.ptrsize == 4:
            value = r.value & 0xffffffff
            value = "0x" + enhex(struct.pack('%sI' % (endian), value))
        elif arch.ptrsize == 8:
            value = r.value & 0xffffffffffffffff
            value = "0x" + enhex(struct.pack('%sQ' % (endian), value))
        else:
            raise
        name = color.reg_name(r.name.rjust(4, ' '))
        value = color.reg_value(value)
        sys.stdout.write("%s: %s " % (name, value))
        i += 1
    print()

@GDBCommand
def code():
    print(color.banner('code'))
    result = disasm_pc(register.pc.value, config.context.code_s)

    while len(result) < config.context.code_s:
        result.append('(bad)')

    i = 0
    for line in result:
        print(line)
        i += 1
        if i == config.context.code_s:
            break

@GDBCommand
def stack():
    print(color.banner('stack'))
    read_from = register.stack.value - arch.ptrsize * config.context.stack_w
    size = arch.ptrsize * config.context.stack_w * config.context.stack_h
    mem = memory.read(read_from, size).tobytes()

    i = 0
    for _ in range(config.context.stack_h):
        sys.stdout.write("%s: " % color.stack_adr(hex(read_from + i)))
        for _ in range(config.context.stack_w):
            data = mem[i:i + arch.ptrsize]
            if arch.endian == 'little':
                data = data[::-1]
            if (read_from + i) < register.stack.value:
                val = color.stack_val_freed("0x%s " % enhex(data))
            elif (read_from + i) == register.stack.value:
                val = color.stack_val_sp("0x%s" % enhex(data)) + " "
            else:
                val = color.stack_val_inuse("0x%s " % enhex(data))
            sys.stdout.write(val)
            i += arch.ptrsize
        print()

@GDBCommand
@adbg.modules.events.stop
def context():
    if config.context.reg:
        reg()
    if config.context.code:
        code()
    if config.context.stack:
        stack()
