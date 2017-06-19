from adbg.commands import GDBCommand
import adbg
import adbg.modules.config as GDBConfig
import inspect
import sys

def dump_config():
    i = 0
    for k in GDBConfig.member.keys():
        scope = getattr(GDBConfig, k)
        print(k.center(20, " "))
        for n in GDBConfig.member[k]:
            v = getattr(scope, n)
            if(i % 6 == 5):
                print()
            sys.stdout.write("\033[38;2;253;254;254m%s\033[0m: \033[38;2;218;247;166m%s\033[0m\t" % (n, v))
            i += 1
    print()

@GDBCommand
def config(*argv):
    if len(argv) == 0:
        dump_config()
