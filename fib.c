int fib(int x) {
    return x < 2 ? 1 : fib(x - 2) + fib(x - 1);
}