#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cffi import FFI

ffi = FFI()
ffi.cdef('''
    int fib(int);
''')

rust = ffi.dlopen("target/release/libtcrusty.so")

def fib(num):
    if num < 2:
        return 1
    return fib(num - 2) + fib(num - 1)
