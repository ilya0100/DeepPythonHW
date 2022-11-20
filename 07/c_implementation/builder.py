import cffi


def build_lib():
    builder = cffi.FFI()

    with open("matrix.h", "r", encoding="utf-8") as define:
        builder.cdef(define.read())

    with open("matrix.c", "r", encoding="utf-8") as source:
        builder.set_source("matrix_lib", source.read())

    builder.compile(target="matrix_lib.so")


if __name__ == "__main__":
    build_lib()
