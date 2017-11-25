#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from tools import c_debug, c_release
from tools import rust_debug, rust_release
from tools import run

# ---- RUST -------------------------------------

rfib_rust_debug = rust_debug.rfib
rfib_rust = rust_release.rfib

# ---- C ----------------------------------------

rfib_c_debug = c_debug.rfib
rfib_c = c_release.rfib

# ---- PYTHON -----------------------------------

def rfib_python(n):
    if n <= 2:
        return 1
    return rfib_python(n - 2) + rfib_python(n - 1)


# ---- PYTHON NUMBA -----------------------------

import numba

@numba.jit
def rfib_numba_lazy(n):
    if n <= 2:
        return 1
    return rfib_numba_lazy(n - 2) + rfib_numba_lazy(n - 1)

@numba.jit(numba.int64(numba.int64))
def rfib_numba(n):
    if n <= 2:
        return 1
    return rfib_numba(n - 2) + rfib_numba(n - 1)

RTESTS = (
    'rfib_rust',
    'rfib_c',
    'rfib_numba',
    'rfib_python',
)


N = 30
ARGS = [N]

def main():
    six.print_("Recursive fibonacci tests:")
    r2 = run('rfib', RTESTS, expected=rfib_c(N), repeat=10)


if __name__ == "__main__":
    main()
