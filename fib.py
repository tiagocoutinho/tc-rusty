#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from cffi import FFI

ffi = FFI()
ffi.cdef('int fib(int);')

def get_fib_from_lib(name):
    return ffi.dlopen(name).fib

# ---- RUST -------------------------------------

fibrust_debug = get_fib_from_lib("target/debug/libtcrusty.so")
fibrust_release = get_fib_from_lib("target/release/libtcrusty.so")

# ---- C ----------------------------------------

fibc_debug = get_fib_from_lib("./libfib.debug.so")
fibc_release = get_fib_from_lib("./libfib.release.so")

# ---- PYTHON -----------------------------------

def fibpy(num):
    if num < 2:
        return 1
    return fibpy(num - 2) + fibpy(num - 1)

TESTS = (('rust_debug', fibrust_debug), ('rust_release', fibrust_release),
         ('c_debug', fibc_debug), ('c_release', fibc_release),
         ('py', fibpy))


def timeit(n):
    import time
    for (name, f) in TESTS:
        print("Starting {0}...".format(name))
        s = time.time()
        r = f(n)
        dt = time.time() - s
        print("{0} took {1:g}s".format(name, dt))

if __name__ == "__main__":
    from sys import argv
    n = 35
    if len(argv) > 1:
        n = int(argv[1])
    timeit(n)
