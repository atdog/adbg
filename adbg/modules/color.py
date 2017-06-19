import sys
from types import ModuleType

def parametrized(dec):
    def decorator(*args, **kwargs):
        def wrapper(f):
            return dec(f, *args, **kwargs)
        return wrapper
    return decorator

@parametrized
def RGB(f, r, g, b):
    post = "\033[0m"
    pre = "\033[38;2;%d;%d;%dm" % (r, g, b)
    def decorator(*args, **kwargs):
        value = f(*args, **kwargs)
        return pre + value + post
    return decorator

class module(ModuleType):

    @RGB(133, 193, 233)
    def prompt(self, value):
        return value

    @RGB(253, 254, 254)
    def key(self, value):
        return value

    @RGB(218, 247, 166)
    def value(self, v):
        return v

    @RGB(218, 247, 166)
    def title(self, value):
        return value

sys.modules[__name__] = module(__name__)
