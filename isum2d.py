import six
import numpy

from tools import GCContext, run
from tools import c_debug, c_release
from tools import rust_debug, rust_release


# ---- PYTHON -----------------------------------

def sum2d_python(arr, m, n):
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += arr[i,j]
    return result

def sum2d_numpy(arr, m, n):
    return arr.sum()


# ---- PYTHON NUMBA -----------------------------

import numba

#@numba.jit(numba.int64(numba.int64[:], numba.int64, numba.int64))
@numba.jit
def sum2d_numba(arr, m, n):
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += arr[i,j]
    return result


# ---- PYTHON PYTHRAN ---------------------------

from pythrantcrusty import sum2d_pythran


# ---- Main -------------------------------------

N = 1000
data = numpy.arange(N**2).reshape(N, N)
ARGS = data, data.shape[0], data.shape[1]

def main():
    TESTS = (
#        'sum2d_rust',
#        'sum2d_c',
        'sum2d_numba',
        'sum2d_pythran',
        'sum2d_python',
        'sum2d_numpy',
    )

    expected = sum2d_numpy(*ARGS)
    run('sum2d', TESTS, expected=expected, repeat=100)


if __name__ == "__main__":
    main()
