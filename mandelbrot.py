from __future__ import division

import numpy

from tools import run
from tools import c_debug, c_release
from tools import rust_debug, rust_release


# ---- PYTHON ----------------------------------

def mandel_python(x, y, max_iters):
    i = 0
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 255

def fractal_python(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel_python(real, imag, iters)
            image[y, x] = color
    return image


# ---- PYTHON NUMBA -----------------------------

import numba

@numba.jit
def mandel_numba(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    i = 0
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 255

@numba.jit
def fractal_numba(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel_numba(real, imag, iters)
            image[y, x] = color
    return image

# ---- PYTHON PYTHRAN ---------------------------

from pythrantcrusty import fractal_pythran

# ---- Main -------------------------------------

image = numpy.zeros((500 * 2, 750 * 2), dtype=numpy.uint8)
ARGS = -2.0, 1.0, -1.0, 1.0, image, 20

def main():
    TESTS = (
        'fractal_numba',
        'fractal_pythran',
        'fractal_python',
    )

    expected = image.copy()
    args = list(ARGS)
    args[-2] = expected
    fractal_numba(*args)
    run('mandelbrot', TESTS, expected=expected, repeat=1)


if __name__ == "__main__":
    main()
