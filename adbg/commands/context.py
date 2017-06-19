from adbg.commands import GDBCommand
import adbg
import adbg.modules.config as config

config.boolean('context', 'reg', "on")
config.boolean('context', 'stack', "on")
config.boolean('context', 'code', "on")

@GDBCommand
@adbg.modules.events.stop
def context():
    print('test')
