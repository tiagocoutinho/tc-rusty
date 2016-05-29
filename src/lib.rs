#![crate_type = "dylib"]

#[no_mangle]
pub extern fn fib(x: i32) -> i32 {
    if x < 2 { 1 } else { fib(x - 2) + fib(x - 1) }
}

#[test]
fn test_fib() {
    assert!(fib(1) == 1);
    assert!(fib(2) == 2);
    assert!(fib(3) == 3);
}
