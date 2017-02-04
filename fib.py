#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
import time

from cffi import FFI


class GCContext(object):

    def __enter__(self):
        gc.disable()
    def __exit__(self, *args):
        gc.enable()


ffi = FFI()
ffi.cdef('int64_t fib(int64_t); int rfib(int64_t);')

def get_fibs_from_lib(lib_name):
    lib = ffi.dlopen(lib_name)
    return lib.fib, lib.rfib

# ---- RUST -------------------------------------

fibrust_debug, rfibrust_debug = get_fibs_from_lib("target/debug/libtcrusty.so")
fibrust_release, rfibrust_release = get_fibs_from_lib("target/release/libtcrusty.so")

# ---- C ----------------------------------------

fibc_debug, rfibc_debug = get_fibs_from_lib("./libfib.debug.so")
fibc_release, rfibc_release = get_fibs_from_lib("./libfib.release.so")

# ---- PYTHON -----------------------------------

def fibpy(n):
    i, sum, last, curr = 0, 0, 0, 1
    if n <= 2:
        return 1
    while i < n - 1:
        sum = last + curr
        last = curr
        curr = sum
        i += 1
    return sum


def rfibpy(n):
    if n <= 2:
        return 1
    return rfibpy(n - 2) + rfibpy(n - 1)


# ---- PYTHON NUMBA -----------------------------

import numba

@numba.jit
def fibnumba_lazy(n):
    i, sum, last, curr = 0, 0, 0, 1
    if n <= 2:
        return 1
    while i < n - 1:
        sum = last + curr
        last = curr
        curr = sum
        i += 1
    return sum

@numba.jit(numba.int64(numba.int64))
def fibnumba_eager(n):
    i, sum, last, curr = 0, 0, 0, 1
    if n <= 2:
        return 1
    while i < n - 1:
        sum = last + curr
        last = curr
        curr = sum
        i += 1
    return sum

@numba.jit
def rfibnumba_lazy(n):
    if n <= 2:
        return 1
    return rfibnumba_lazy(n - 2) + rfibnumba_lazy(n - 1)

@numba.jit(numba.int64(numba.int64))
def rfibnumba_eager(n):
    if n <= 2:
        return 1
    return rfibnumba_eager(n - 2) + rfibnumba_eager(n - 1)

TESTS = (
    ('rust_debug', fibrust_debug),
    ('rust_release', fibrust_release),
    ('c_debug', fibc_debug),
    ('c_release', fibc_release),
    ('numba lazy', fibnumba_lazy),
    ('numba_eager', fibnumba_eager),
    ('py', fibpy)
)

RTESTS = (
    ('rust_debug', rfibrust_debug),
    ('rust_release', rfibrust_release),
    ('c_debug', rfibc_debug),
    ('c_release', rfibc_release),
    ('numba lazy', rfibnumba_lazy),
    ('numba_eager', rfibnumba_eager),
    ('py', rfibpy)
)

def timeall(tests, n=30, verbose=True):
    results = {}
    for (name, f) in tests:
        dt = simple_fib_timeit(f, n)
        results[name] = dt
    if verbose:
        for name in sorted(results, key=lambda x: results[x]):
            print("{0} took {1:g}s".format(name, results[name]))
    return results

def simple_fib_timeit(f, fib_number=30):
    with GCContext():
        s = time.time()
        r = f(fib_number)
        return time.time() - s

if __name__ == "__main__":
    from sys import argv

    N = 35
    if len(argv) > 1:
        N = int(argv[1])

    print "Functional fibonacci tests:"
    r1 = timeall(TESTS, 90)
    print
    print "Recursive fibonacci tests:"
    r2 = timeall(RTESTS, N)

    import numpy
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    x = numpy.arange(len(r2))

    names = sorted(r2, key=lambda x: r2[x])
    y = [r2[k] for k in names]
    rects1 = ax.bar(x, y, color='r')
    ax.set_xticks(x)
    ax.set_xticklabels(names)

    plt.show()
