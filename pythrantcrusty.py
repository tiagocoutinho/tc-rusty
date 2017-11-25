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

