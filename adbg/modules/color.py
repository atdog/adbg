import sys
from types import ModuleType

# constant for terminal color code style
NORMAL = 0
BOLD = 1
DIM = 2
UNDERLINED = 4
BLINK = 5
REVERSE = 7
HIDDEN = 8

# decorators
def parametrized(dec):
    def decorator(*args, **kwargs):
        def wrapper(f):
            return dec(f, *args, **kwargs)
        return wrapper
    return decorator

@parametrized
def STYLE(f, r, g, b, s=[]):
    c = ""
    for i in s:
        c += "%d;" % (i)

    post = "\033[0m"
    pre = "\033[%s38;2;%d;%d;%dm" % (c, r, g, b)
    def decorator(*args, **kwargs):
        value = f(*args, **kwargs)
        return pre + value + post
    return decorator

class module(ModuleType):

    @STYLE(133, 193, 233)
    def prompt(self, value):
        return value

    @STYLE(253, 254, 254, [BOLD])
    def key(self, value):
        return value

    @STYLE(218, 247, 166)
    def value(self, v):
        return v

    @STYLE(218, 247, 166)
    def title(self, value):
        return value

sys.modules[__name__] = module(__name__)
