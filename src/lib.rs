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

#[no_mangle]
pub extern fn count_doubles(val: &[u8], n: usize) -> i32 {
    let l = val.len() - 1;
    let mut total: i32 = 0;
    let mut last: u8 = val[0];
    let mut i: usize = 1;
    while i < l {
        if last == val[i] {
            total += 1;
        }
        last = val[i];
        i += 1;
    }
    total
}


#[test]
fn test_rfib() {
    assert!(rfib(1) == 1);
    assert!(rfib(2) == 2);
    assert!(rfib(3) == 3);
}



