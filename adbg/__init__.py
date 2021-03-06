#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gdb

# import global function first
import adbg.modules.utils

import adbg.modules.color as color
import adbg.modules.exception
import adbg.modules.events
import adbg.modules.config
import adbg.modules.proc
import adbg.modules.arch
import adbg.modules.register
import adbg.modules.memory

import adbg.commands

prompt = color.prompt("➜  ")

pre_commands = """
set confirm off
set verbose off
set prompt %s
set height 0
set history expansion on
set history save on
set follow-fork-mode parent
set backtrace past-main on
set step-mode on
set print pretty on
set width 0
set print elements 15
handle SIGALRM nostop print nopass
handle SIGBUS  stop   print nopass
handle SIGPIPE nostop print nopass
handle SIGSEGV stop   print nopass
""".strip() % prompt

for line in pre_commands.strip().splitlines():
    gdb.execute(line)

# This may throw an exception, see pwndbg/pwndbg#27
try:
    gdb.execute("set disassembly-flavor intel")
except gdb.error:
    pass
