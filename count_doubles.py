#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import string
import itertools
import functools

import six
import numpy

from tools import GCContext, run
from tools import c_debug, c_release
from tools import rust_debug, rust_release


# ---- RUST -------------------------------------

count_doubles_rust_debug = rust_debug.count_doubles
count_doubles_rust = rust_release.count_doubles

# ---- C ----------------------------------------

count_doubles_c_debug = c_debug.count_doubles
count_doubles_c = c_release.count_doubles

# ---- PYTHON -----------------------------------

def count_doubles_python(val, n):
    total = 0
    for c1, c2 in itertools.izip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total

# ---- PYTHON NUMBA -----------------------------

import numba

def numba_numpy(f):
    @functools.wraps(f)
    def wrapper(val, n):
        val = numpy.frombuffer(val, dtype=numpy.uint8)
        return f(val, n)
    return wrapper

@numba_numpy
@numba.jit
def count_doubles_numba(val, n):
    total = 0
    for c1, c2 in zip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total

# ---- PYTHON PYTHRAN ---------------------------

from pythrantcrusty import count_doubles_pythran, count_doubles_pythran_zip


# -----------------------------------------------

def get_data():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(this_dir, 'count_doubles.data')
    if os.path.isfile(data_file):
        with open(data_file, 'rb') as f:
            data = f.read()
    else:
        six.print_('Generating data...', end='', flush=True)
        N = 10000000
        data = ''.join(random.choice(string.ascii_letters)
                       for i in range(N))
        with open(data_file, 'wb') as f:
            f.write(data)
        six.print_('[DONE]')
    return data

data = get_data()
ARGS = [data, len(data)]

def main():
    TESTS = (
        'count_doubles_rust',
        'count_doubles_c',
        'count_doubles_numba',
        'count_doubles_pythran',
        'count_doubles_python',
    )

    expected = count_doubles_c(*ARGS)
    run('count_doubles', TESTS, expected=expected, repeat=10)


if __name__ == "__main__":
    main()
