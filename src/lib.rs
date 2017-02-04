#![crate_type = "dylib"]

#[no_mangle]
pub extern fn rfib(n: i64) -> i64 {
    if n <= 2 { 1 } else { rfib(n - 2) + rfib(n - 1) }
}

#[no_mangle]
pub extern fn fib(n: i64) -> i64 {
    if n <= 2 {
        return 1
    }

    let mut i: i64 = 0;
    let mut sum: i64 = 0;
    let mut last: i64 = 0;
    let mut curr: i64 = 1;
    while i < n -1 {
        sum = last + curr;
        last = curr;
        curr = sum;
        i += 1;
    }
    sum
}

#[test]
fn test_rfib() {
    assert!(rfib(1) == 1);
    assert!(rfib(2) == 2);
    assert!(rfib(3) == 3);
}
