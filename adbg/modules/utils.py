import sys
import builtins
import binascii

def ___enhex(value):
    if type(value) is str:
        value = bytes(value, 'utf-8')

    if type(value) is not bytes:
        raise

    v = binascii.hexlify(value)
    return str(v, 'utf-8')

for name in dir(sys.modules[__name__]):
    if not name.startswith('___'):
        continue
    func = getattr(sys.modules[__name__], name)
    setattr(builtins, name[3:], func)
