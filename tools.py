# -*- coding: utf-8 -*-

import gc
import time

import numpy
from cffi import FFI
from matplotlib import pyplot


ffi = FFI()
ffi.cdef("""
int64_t fib(int64_t);
int32_t rfib(int64_t);
int32_t count_doubles(const char *, int);
""")


def get_lib(lib_name):
    return ffi.dlopen(lib_name)


rust_debug = get_lib("target/debug/libtcrusty.so")
rust_release = get_lib("target/release/libtcrusty.so")

c_debug = get_lib("./libctcrusty.debug.so")
c_release = get_lib("./libctcrusty.release.so")


class GCContext(object):

    def __enter__(self):
        gc.disable()
    def __exit__(self, *args):
        gc.enable()


def timeall(tests, args, verbose=True):
    results = {}
    for (name, f) in tests:
        dt = simple_timeit(f, args)
        results[name] = dt
    if verbose:
        for name in sorted(results, key=lambda x: results[x]):
            print("{0} took {1:g}s".format(name, results[name]))
    return results


def simple_timeit(f, args):
    with GCContext():
        s = time.time()
        r = f(*args)
        return time.time() - s


def run(tests, args=(), verbose=True):
    result = timeall(tests, args, verbose=verbose)
    ax = pyplot.subplot()
    x = numpy.arange(len(result))

    names = sorted(result, key=lambda x: result[x])
    y = [result[k] for k in names]
    rects1 = ax.bar(x, y, color='r')
    ax.set_xticks(x)
    ax.set_xticklabels(names)

    pyplot.show()

    return result
