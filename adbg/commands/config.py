import inspect
import sys

import adbg
import adbg.modules.config as GDBConfig
import adbg.modules.color as color
from adbg.commands import GDBCommand

def dump_config():
    i = 0
    for k in GDBConfig.member.keys():
        scope = getattr(GDBConfig, k)
        print(k.center(20, " "))
        for n in GDBConfig.member[k]:
            v = getattr(scope, n)
            if(i % 6 == 5):
                print()
            sys.stdout.write("%s: %s\t" % (color.key(n), color.value(str(v))))
            i += 1
    print()

@GDBCommand
def config(*argv):
    if len(argv) == 0:
        dump_config()
