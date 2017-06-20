import sys
import gdb
from types import ModuleType

class ConfigProp(object):
    def __init__(self, default):
        self.prop = default
    def __get__(self, obj, objtype):
        return self.prop
    def __set__(self, obj, value):
        self.prop = value

class PropBoolean(ConfigProp):
    def __init__(self, default):
        value = self.sanatize(default)
        super(self.__class__, self).__init__(value)

    def sanatize(self, value):
        if type(value) is str:
            if value.lower() == "on":
                value = True
            elif value.lower() == "off":
                value = False
            else:
                value = int(value)
        elif type(value) is bool:
            return value
        else:
            value = -1

        if value < 0 or value > 1:
            print('value must be boolean (0 or 1)')
            raise AttributeError

        if value == 1:
            value = True
        else:
            value = False

        return value

    def __set__(self, obj, value):
        value = self.sanatize(value)
        # default setter
        super(self.__class__, self).__set__(obj, value)

class PropInt(ConfigProp):
    def __init__(self, default):
        value = self.sanatize(default)
        super(self.__class__, self).__init__(value)

    def sanatize(self, value):
        value = int(value)
        return value

    def __set__(self, obj, value):
        value = self.sanatize(value)
        # default setter
        super(self.__class__, self).__set__(obj, value)

def ClassFactory(name, base=ModuleType):
    newclass = type(name, (base,), {})
    return newclass

def scope_prop(f):
    def wrapper(*args):
        self, scope_name, key, value = args
        prop = f(*args)
        scope_class = self.get_scope_class(scope_name)
        self.member[scope_name].append(key)
        setattr(scope_class, key, prop)
    return wrapper

class module(ModuleType):
    def __init__(self, name):
        self.name = name
        super(module, self).__init__(name)

    # hold class type
    _class = {}
    member = {}
    def get_scope_class(self, scope):
        if scope not in dir(module):
            scope_class = ClassFactory(scope)
            setattr(module, scope, scope_class(scope))
            self.member[scope] = []
            self._class[scope] = scope_class
        else:
            scope_class = self._class[scope]
        return scope_class

    @scope_prop
    def boolean(self, scope, name, default):
        return PropBoolean(default)

    @scope_prop
    def int(self, scope, name, default):
        return PropInt(default)

sys.modules[__name__] = module(__name__)
