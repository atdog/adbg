from os import path

directory, file = path.split(__file__)
directory       = path.expanduser(directory)
directory       = path.abspath(directory)

print("Add system path: {}".format(directory))
sys.path.append(directory)

import adbg
