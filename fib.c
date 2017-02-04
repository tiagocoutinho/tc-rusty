#include <stdint.h>

int rfib(int64_t n) {
    return n <= 2 ? 1 : rfib(n - 2) + rfib(n - 1);
}

int fib(int64_t n) {
    int64_t i = 0, sum = 0, last = 0, curr = 1;
    if (n <= 2)
        return 1;

    while(i < n - 1) {
        sum = last + curr;
        last = curr;
        curr = sum;
        i += 1;
    }
    return sum;
}
