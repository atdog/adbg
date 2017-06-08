from adbg.commands import GDBCommand
from adbg.modules import proc
import subprocess
import gdb

@GDBCommand
def at(processname=None):
    if processname is None:
        print("Please specify a proc name")
        return

    try:
        pidlist = map(int, subprocess.check_output('pidof $(basename {})'.format(processname), shell=True).decode('utf8').split())

        for pid in pidlist:
            if pid == proc.pid:
                continue
            print('attaching to {} ...'.format(processname))
            gdb.execute("attach {}".format(pid))
            return

        print("already attached on {}".format(proc.pid))
    except Exception as e:
        print(e)
