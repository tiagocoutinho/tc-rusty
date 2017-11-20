build: build-c build-rust build-pythran

build-rust:
	cargo build
	cargo build --release

build-c:
	$(CC) -c -fPIC ctcrusty.c -o ctcrusty.o
	$(CC) -shared -Wl,-soname,libctcrusty.so.1 -o libctcrusty.debug.so ctcrusty.o
	rm ctcrusty.o
	$(CC) -O3 -c -fPIC ctcrusty.c -o ctcrusty.o
	$(CC) -O3 -shared -Wl,-soname,libctcrusty.so.1 -o libctcrusty.release.so ctcrusty.o
	rm ctcrusty.o

build-pythran:
	pythran pythrantcrusty.py

test: build
	python fib.py

clean:
	rm -rf ctcrusty.o libctcrusty.debug.so libctcrusty.release.so libctcrusty.so
	rm -rf pythranrusty.so
	cargo clean
