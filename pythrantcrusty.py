#pythran export fib_pythran(int)
def fib_pythran(n):
    i, sum, last, curr = 0, 0, 0, 1
    if n <= 2:
        return 1
    while i < n - 1:
        sum = last + curr
        last = curr
        curr = sum
        i += 1
    return sum


#pythran export count_doubles_pythran_zip(str, int)
def count_doubles_pythran_zip(val, n):
    total = 0
    for c1, c2 in zip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


#pythran export count_doubles_pythran(str, int)
def count_doubles_pythran(val, n):
    total = 0
    last = val[0]
    for i in range(1, n):
        cur = val[i]
        if last == cur:
            total += 1
        last = cur
    return total

#pythran export sum2d_pythran(int[][], int, int)
def sum2d_pythran(arr, m, n):
    result = 0.0
    for i in range(m):
        for j in range(n):
            result += arr[i,j]
    return result


#pythran export mandel_pythran(int, int, int)
def mandel_pythran(x, y, max_iters):
    i = 0
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 255


#pythran export fractal_pythran(float, float, float, float, uint8[][], int)
def fractal_pythran(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel_pythran(real, imag, iters)
            image[y, x] = color
    return image
