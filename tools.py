# -*- coding: utf-8 -*-

import gc
import time
import timeit

import six
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


def timeall(mod_name, tests, expected, repeat=1000, verbose=True):
    results = {}
    for name in tests:
        if verbose:
            msg = 'Started {0} (N={1})... '.format(name, repeat)

            six.print_('{0: <80}'.format(msg), end='', flush=True)
        dt = simple_timeit(mod_name, name, expected, repeat)
        results[name] = dt
        if verbose:
            print("[DONE] {1:g}s/iteration".format(name, dt))

    return results


def simple_timeit(mod_name, fname, expected, repeat):
    setup = 'from {0} import ARGS, {1}'.format(mod_name, fname)
    stmt = '{0}(*ARGS)'.format(fname)

    # run once to assert result
    rmap = {}
    exec('{setup}\nr = {stmt}'.format(setup=setup, stmt=stmt), rmap)
    r = rmap['r']
    assert numpy.all(r == expected), \
            "expected {0} for {1}. Got {2}".format(expected, fname, r)
    total_time = timeit.timeit(setup=setup, stmt=stmt, number=repeat)
    return total_time / float(repeat)


def run(mod_name, tests, expected=None, repeat=1000, verbose=True):
    result = timeall(mod_name, tests, expected, repeat=repeat,
                     verbose=verbose)
    plot(mod_name, result)


def simple_plot(title, result):
    ax = pyplot.subplot(title=title)
    names = sorted(result, key=lambda x: result[x])
    labels = [name.rsplit('_', 1)[-1] for name in names]
    x = numpy.arange(len(result))
    y = numpy.array([result[k] for k in names])
    ax.bar(x, y, color='g')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('time (s) - less is better')
    pyplot.show()


def plot(title, result):
    fig, (left, right) = pyplot.subplots(ncols=2)

    names = sorted(result, key=lambda x: result[x])
    # remove worst
    worst_name = names[-1]
    worst_value = result.pop(worst_name)
    worst_label = worst_name.rsplit('_', 1)[-1]
    names = names[:-1]
    labels = [name.rsplit('_', 1)[-1] for name in names]
    x = numpy.arange(len(result))
    y = numpy.array([result[k] for k in names])

    left_y = y
    left.bar(x, left_y, color='g')
    left.set_title('{0}\n(omitted slower: {1!r} - {2}s)'.format(title,
                                                                worst_label,
                                                                worst_value))
    left.set_xticks(x)
    left.set_xticklabels(labels)
    left.set_ylabel('time (s) - less is better')

    right_y = worst_value / y
    right.bar(x, right_y, color='b')
    right.set_title('{0}\n(relative to {1!r})'.format(title, worst_label))
    right.set_xticks(x)
    right.set_xticklabels(labels)
    right.set_ylabel('speed boost - more is better')

    pyplot.show()
