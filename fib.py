#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools import GCContext
from tools import c_debug, c_release
from tools import rust_debug, rust_release
from tools import timeall

# ---- RUST -------------------------------------

fib_rust_debug, rfib_rust_debug = rust_debug.fib, rust_debug.rfib
fib_rust_release, rfib_rust_release = rust_release.fib, rust_release.rfib

# ---- C ----------------------------------------

fib_c_debug, rfib_c_debug = c_debug.fib, c_debug.rfib
fib_c_release, rfib_c_release = c_release.fib, c_release.rfib

# ---- PYTHON -----------------------------------

def fib_py(n):
    i, sum, last, curr = 0, 0, 0, 1
    if n <= 2:
        return 1
    while i < n - 1:
        sum = last + curr
        last = curr
        curr = sum
        i += 1
    return sum


def rfib_py(n):
    if n <= 2:
        return 1
    return rfib_py(n - 2) + rfib_py(n - 1)


# ---- PYTHON NUMBA -----------------------------

import numba

@numba.jit
def fib_numba_lazy(n):
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
def fib_numba_eager(n):
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
def rfib_numba_lazy(n):
    if n <= 2:
        return 1
    return rfib_numba_lazy(n - 2) + rfib_numba_lazy(n - 1)

@numba.jit(numba.int64(numba.int64))
def rfib_numba_eager(n):
    if n <= 2:
        return 1
    return rfib_numba_eager(n - 2) + rfib_numba_eager(n - 1)

# ---- PYTHON PYTHRAN ---------------------------

from pythranrusty import fib_pythran


TESTS = (
    ('rust_debug', fib_rust_debug),
    ('rust_release', fib_rust_release),
    ('c_debug', fib_c_debug),
    ('c_release', fib_c_release),
    ('numba lazy', fib_numba_lazy),
    ('numba_eager', fib_numba_eager),
    ('pythran', fib_pythran),
    ('py', fib_py)
)

RTESTS = (
    ('rust_debug', rfib_rust_debug),
    ('rust_release', rfib_rust_release),
    ('c_debug', rfib_c_debug),
    ('c_release', rfib_c_release),
    ('numba lazy', rfib_numba_lazy),
    ('numba_eager', rfib_numba_eager),
#    ('py', rfib_py)
)


if __name__ == "__main__":
    from sys import argv

    N = 35
    if len(argv) > 1:
        N = int(argv[1])

    print "Functional fibonacci tests:"
    r1 = timeall(TESTS, (92,))
    print
    print "Recursive fibonacci tests:"
    r2 = timeall(RTESTS, (N,))

    result = r1

    import numpy
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    x = numpy.arange(len(result))

    names = sorted(result, key=lambda x: result[x])
    y = [result[k] for k in names]
    rects1 = ax.bar(x, y, color='r')
    ax.set_xticks(x)
    ax.set_xticklabels(names)

    plt.show()
