import gdb
import sys
import adbg

def fix_arch(arch):
    arches = ['x86-64', 'i386', 'mips', 'powerpc', 'sparc', 'arm', 'aarch64', arch]
    return next(a for a in arches if a in arch)

@adbg.modules.events.stop
def update():
    m = sys.modules[__name__]
    try:
        m.current = fix_arch(gdb.newest_frame().architecture().name())
    except Exception:
        return

    m.ptrsize = gdb.lookup_type('void').pointer().sizeof
    if 'little' in gdb.execute('show endian', to_string=True):
        m.endian = 'little'
    else:
        m.endian = 'big'
