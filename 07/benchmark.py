from time import time
import cffi

import numpy as np

from matrix import PyMatrix, matrix_mul


ffi = cffi.FFI()
matrix_lib = ffi.dlopen("07/c_implementation/matrix_lib.so")
with open("07/c_implementation/matrix.h", "r", encoding="utf-8") as define:
    ffi.cdef(define.read())


def fill_matrix(cmatrix, source):
    for i in range(cmatrix.rows):
        for j in range(cmatrix.cols):
            matrix_lib.set_elem(cmatrix, i, j, source[i, j])


def main(size=100):
    np_matrix = np.random.random((size, size))
    py_matrix = PyMatrix(size, size, np_matrix.flatten())
    c_matrix = matrix_lib.create_matrix(size, size)
    fill_matrix(c_matrix, np_matrix)

    print("========= Python ========")
    average_time = 0
    for _ in range(10):
        py_start_time = time()
        py_result = matrix_mul(py_matrix, py_matrix)
        py_end_time = time()
        average_time += (py_end_time - py_start_time) / 10
    print(f"Time: {average_time}")

    print("=========== C ===========")
    average_time = 0
    for _ in range(10):
        c_start_time = time()
        c_result = matrix_lib.mul(c_matrix, c_matrix)
        c_end_time = time()
        average_time += (c_end_time - c_start_time) / 10
    print(f"Time: {average_time}")

    print("========= Numpy =========")
    average_time = 0
    for _ in range(10):
        np_start_time = time()
        np_result = np_matrix @ np_matrix
        np_end_time = time()
        average_time += (np_end_time - np_start_time) / 10
    print(f"Time: {average_time}")

    assert py_result.data != list(np_result.flatten())
    assert ffi.unpack(c_result, c_result.rows * c_result.cols) != list(
        np_result.flatten()
    )


if __name__ == "__main__":
    main(300)
