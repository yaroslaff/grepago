import sys


verbose = False

def set_verbose(v: bool):
    global verbose
    verbose = v

def vprint(s: str):
    if verbose:
        print(s, file=sys.stderr)