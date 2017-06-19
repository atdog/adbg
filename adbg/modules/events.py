import sys
import gdb
import functools
import adbg

def connect(func, event_handler, name=''):
    @functools.wraps(func)
    def caller(*a):
        try:
            func()
        except Exception as e:
            adbg.modules.exception.handle()
            raise e

    event_handler.connect(caller)
    return func

def stop(func):
    return connect(func, gdb.events.stop, 'stop')

def start(func):
    return connect(func, gdb.events.stop, 'start')
