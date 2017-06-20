from adbg.commands import GDBCommand
import os
import stat

def which(name, all = False):
    # If name is a path, do not attempt to resolve it.
    if os.path.sep in name:
        return name

    isroot = os.getuid() == 0
    out = set()
    try:
        path = os.environ['PATH']
    except KeyError:
        log.exception('Environment variable $PATH is not set')
    for p in path.split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, os.X_OK):
            st = os.stat(p)
            if not stat.S_ISREG(st.st_mode):
                continue
            # work around this issue: https://bugs.python.org/issue9311
            if isroot and not \
              st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                continue
            if all:
                out.add(p)
            else:
                return p
    if all:
        return out
    else:
        return None

shellcmds = [
    "asm", # pwntools
    "awk",
    "bash",
    "cat",
    "chattr",
    "chmod",
    "chown",
    # "clear",
    "constgrep", # pwntools
    "cp",
    "cyclic", # pwntools
    "date",
    "diff",
    "egrep",
    # "find", don't expose find as its an internal gdb command
    "grep",
    "htop",
    "id",
    # "kill",
    # "killall",
    "less",
    # "ln",
    "ls",
    "man",
    "mkdir",
    "mktemp",
    "more",
    "mv",
    "nano",
    "nc",
    "ping",
    "pkill",
    "ps",
    "pstree",
    "pwd",
    "rm",
    "sed",
    "sh",
    "sort",
    "ssh",
    "sudo",
    "tail",
    "top",
    "touch",
    "unhex", # pwntools
    "uniq",
    "vi",
    "vim",
    "w",
    "wget",
    "who",
    "whoami",
    "zsh",
]

shellcmds = filter(which, shellcmds)

def register_shell_function(cmd):
    def handler(*a):
        """Invokes %s""" % cmd
        if os.fork() == 0:
            os.execvp(cmd, (cmd,) + a)
        os.wait()
    handler.__name__ = str(cmd)
    GDBCommand(handler)

for cmd in shellcmds:
    register_shell_function(cmd)
