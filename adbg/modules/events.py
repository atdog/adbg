import sys
import gdb
import functools

def connect(func, event_handler, name=''):
    @functools.wraps(func)
    def caller(*a):
        try:
            func()
        except Exception as e:
            pwndbg.exception.handle()
            raise e

    event_handler.connect(caller)
    return func

def stop(func):
    return connect(func, gdb.events.stop, 'stop')

