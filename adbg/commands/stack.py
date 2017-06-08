from adbg.commands import GDBCommand
import adbg.modules.events

@GDBCommand
@adbg.modules.events.stop
def stack():
    print('test')
