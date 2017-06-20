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
def STYLE(f, code, *s):
    c = ""
    for i in s:
        c += "%d;" % (i)

    code = int(code[1:], 16)
    r = code >> 16 & 0x0ff
    g = code >> 8 & 0x0ff
    b = code & 0x0ff

    post = "\033[0m"
    pre = "\033[%s38;2;%d;%d;%dm" % (c, r, g, b)
    def decorator(*args, **kwargs):
        value = f(*args, **kwargs)
        return pre + value + post
    return decorator

class module(ModuleType):

    @STYLE('#85C1E9')
    def prompt(self, value):
        return value

    @STYLE('#FDFEFE', BOLD)
    def key(self, value):
        return value

    @STYLE('#DAF7A6')
    def value(self, v):
        return v

    @STYLE('#F5B041', BOLD)
    def title(self, value):
        return value

    @STYLE('#CACFD2')
    def stack_val_freed(self, value):
        return value

    @STYLE('#CACFD2', BOLD)
    def stack_val_inuse(self, value):
        return value

    @STYLE('#ABEBC6', BOLD, UNDERLINED)
    def stack_val_sp(self, value):
        return value

    @STYLE('#F9E79F', BOLD)
    def stack_adr(self, value):
        return value

    @STYLE('#EC7063', BOLD)
    def code_adr(self, value):
        return value

    @STYLE('#D7BDE2', BOLD)
    def code_val_pc(self, value):
        return value

    @STYLE('#A9DFBF', BOLD)
    def reg_name(self, value):
        return value

    @STYLE('#C2CFD2', BOLD)
    def reg_value(self, value):
        return value

    @STYLE('#E59866', BOLD)
    def banner(self, value):
        value = " " + value + " "
        return value.center(20, '-')

sys.modules[__name__] = module(__name__)
