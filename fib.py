#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from tools import c_debug, c_release
from tools import rust_debug, rust_release
from tools import run

# ---- RUST -------------------------------------

fib_rust_debug = rust_debug.fib
fib_rust = rust_release.fib

# ---- C ----------------------------------------

fib_c_debug = c_debug.fib
fib_c = c_release.fib

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
def fib_numba(n):
    i, sum, last, curr = 0, 0, 0, 1
    if n <= 2:
        return 1
    while i < n - 1:
        sum = last + curr
        last = curr
        curr = sum
        i += 1
    return sum


# ---- PYTHON PYTHRAN ---------------------------

from pythrantcrusty import fib_pythran


TESTS = (
    'fib_py',
#    'fib_rust_debug',
    'fib_rust',
#    'fib_c_debug',
    'fib_c',
    'fib_numba',
    'fib_pythran',
)

N = 92
ARGS = [N]

def main():
    six.print_("Functional fibonacci tests:")
    r1 = run('fib', TESTS, expected=fib_py(N), repeat=100000)


if __name__ == "__main__":
    main()
