from adbg.commands import GDBCommand
import subprocess
import adbg.modules.proc
import gdb

@GDBCommand
def at(processname=None):
    if processname is None:
        print("Please specify a proc name")
        return

    try:
        pidlist = map(int, subprocess.check_output('pidof $(basename {})'.format(processname), shell=True).decode('utf8').split())

        for pid in pidlist:
            if pid == adbg.modules.proc.pid:
                continue
            print('attaching to {} ...'.format(processname))
            gdb.execute("attach {}".format(pid))
            return

        print("already attached on {}".format(pwndbg.proc.pid))
    except Exception as e:
        print(e)
