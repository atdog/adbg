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
        super(PropBoolean, self).__init__(value)

    def sanatize(self, value):
        if type(value) is str:
            if value.lower() == "on":
                value = True
            elif value.lower() == "off":
                value = False
            else:
                value = -1
        elif type(value) is not int:
            value = -1

        if value < 0 or value > 1:
            print('value must be boolean (0 or 1)')
            raise AttributeError

        return value

    def __set__(self, obj, value):
        value = self.sanatize(value)
        # default setter
        super(PropBoolean, self).__set__(obj, value)

def ClassFactory(name, base=ModuleType):
    newclass = type(name, (base,),{})
    return newclass

class module(ModuleType):
    def __init__(self, name):
        self.name = name
        super(module, self).__init__(name)

    member = {}
    def get_scope_class(self, scope):
        if scope not in dir(module):
            self.member[scope] = []
            scope_class = ClassFactory(scope)
            setattr(module, scope, scope_class)
        else:
            scope_class = getattr(module, scope)
        return scope_class

    def boolean(self, scope, name, default):
        scope_class = self.get_scope_class(scope)
        self.member[scope].append(name)
        setattr(scope_class, name, PropBoolean(default))

sys.modules[__name__] = module(__name__)
