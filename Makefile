build: build-c build-rust

build-rust:
	cargo build
	cargo build --release

build-c:
	$(CC) -c -fPIC fib.c -o fib.o
	$(CC) -shared -Wl,-soname,libfib.so.1 -o libfib.debug.so fib.o
	rm fib.o
	$(CC) -O2 -c -fPIC fib.c -o fib.o
	$(CC) -O2 -shared -Wl,-soname,libfib.so.1 -o libfib.release.so fib.o
	rm fib.o

test: build
	python fib.py

clean:
	rm -f fib.o libfib.debug.so libfib.so

