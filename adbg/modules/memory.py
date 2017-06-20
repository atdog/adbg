import gdb

def read(addr, size):
    inferior = gdb.selected_inferior()
    return inferior.read_memory(addr, size)
