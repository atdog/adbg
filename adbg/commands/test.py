#example 1
from adbg.commands import GDBCommand

@GDBCommand
def test1():
    print('Test() without args')

# example 2
from adbg.commands import GDBCommandWithArgParser
import argparse

options = ['1', '2', '3']

parser = argparse.ArgumentParser(description='Test Description')
parser.add_argument('state', nargs='?', type=str, choices=options,
                    help="Help message")

@GDBCommandWithArgParser(parser)
def test2(state=None):
    print('Test() with arg parser')
