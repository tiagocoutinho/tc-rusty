#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import itertools


from tools import GCContext, run
from tools import c_debug, c_release
from tools import rust_debug, rust_release


# ---- RUST -------------------------------------

count_doubles_rust_debug = rust_debug.count_doubles
count_doubles_rust_release = rust_release.count_doubles

# ---- C ----------------------------------------

count_doubles_c_debug = c_debug.count_doubles
count_doubles_c_release = c_release.count_doubles

# ---- PYTHON -----------------------------------

def count_doubles_py(val):
    total = 0
    for c1, c2 in zip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


def icount_doubles_py(val):
    total = 0
    for c1, c2 in itertools.izip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


# ---- PYTHON NUMBA -----------------------------

import numba

@numba.jit
def count_doubles_numba_lazy(val):
    total = 0
    for c1, c2 in zip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


@numba.jit
def icount_doubles_numba_lazy(val):
    total = 0
    for c1, c2 in itertools.izip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


@numba.jit
def count_doubles_numba_specialized(val):
    total = 0
    l = len(val)
    last = val[0]
    for i in range(1, l):
        cur = val[i]
        if last == cur:
            total += 1
        last = cur
    return total


# ---- PYTHON PYTHRAN ---------------------------

from pythrantcrusty import (count_doubles_pythran,
                            icount_doubles_pythran,
                            count_doubles_pythran_specialized)

# -----------------------------------------------

if __name__ == "__main__":
    N = 10000000
    data = ''.join(random.choice(string.ascii_letters)
                   for i in range(N))

    TESTS = (
#        ('rust_debug', count_doubles_rust_debug),
#        ('rust_release', count_doubles_rust_release),
        ('c_debug', lambda x: count_doubles_c_debug(x, N)),
        ('c_release', lambda x: count_doubles_c_release(x, N)),
        ('numba lazy', count_doubles_numba_lazy),
        ('inumba lazy', icount_doubles_numba_lazy),
        ('numba specialized', count_doubles_numba_specialized),
        #    ('numba_eager', count_doubles_numba_eager),
        ('pt', count_doubles_pythran),
        ('ipt', icount_doubles_pythran),
        ('pt_specialized', count_doubles_pythran),
        ('py', count_doubles_py),
        ('ipy', icount_doubles_py),
    )

    ref = count_doubles_py(data)
    for name, f in TESTS:
        assert ref == f(data)

    run(TESTS, (data,))
