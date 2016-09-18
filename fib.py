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

# ---- PYTHON NUMBA -----------------------------

import numba

@numba.jit
def fibnumba_lazy(num):
    if num < 2:
        return 1
    return fibnumba_lazy(num - 2) + fibnumba_lazy(num - 1)

#fibnumba_eager = numba.jit(fibpy, numba.int64(numba.int64))
@numba.jit(numba.int64(numba.int64))
def fibnumba_eager(num):
    if num < 2:
        return 1
    return fibnumba_eager(num - 2) + fibnumba_eager(num - 1)

@numba.jit(nogil=True)
def fibnumba_lazy_nogil(num):
    if num < 2:
        return 1
    return fibnumba_lazy_nogil(num - 2) + fibnumba_lazy_nogil(num - 1)

#fibnumba_eager = numba.jit(fibpy, numba.int64(numba.int64))
@numba.jit(numba.int64(numba.int64), nogil=True)
def fibnumba_eager_nogil(num):
    if num < 2:
        return 1
    return fibnumba_eager_nogil(num - 2) + fibnumba_eager_nogil(num - 1)


TESTS = (
    ('rust_debug', fibrust_debug),
    ('rust_release', fibrust_release),
    ('c_debug', fibc_debug),
    ('c_release', fibc_release),
    ('numba lazy', fibnumba_lazy),
    ('numba_eager', fibnumba_eager),
    ('numba lazy_nogil', fibnumba_lazy_nogil),
    ('numba_eager_nogil', fibnumba_eager_nogil),
    ('py', fibpy)
)

def timeall(n, verbose=True):
    for (name, f) in TESTS:
#        if verbose: print("Starting {}...".format(name))
        dt = timeit(f, n)
        if verbose:print("{0} took {1:g}s".format(name, dt))

def timeit(f, n):
    s = time.time()
    r = f(n)
    return time.time() - s

if __name__ == "__main__":
    from sys import argv
    n = 30
    if len(argv) > 1:
        n = int(argv[1])

    # warm up
#    timeall(3, verbose=False)

    timeall(n)
