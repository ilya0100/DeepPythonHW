from unittest import TestCase

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


class TestMatrix(TestCase):
    cases = [
        {
            "l": np.array(np.arange(1, 10), dtype=float).reshape(3, 3),
            "r": np.array(np.arange(1, 10), dtype=float).reshape(3, 3),
        },
        {
            "l": np.array(np.arange(1, 7), dtype=float).reshape(2, 3),
            "r": np.array(np.arange(1, 7), dtype=float).reshape(3, 2),
        },
        {
            "l": np.array(np.arange(1, 11), dtype=float).reshape(1, 10),
            "r": np.array(np.arange(1, 11), dtype=float).reshape(10, 1),
        },
        {
            "r": np.array(np.arange(1, 11), dtype=float).reshape(10, 1),
            "l": np.array(np.arange(1, 11), dtype=float).reshape(1, 10),
        },
    ]

    def test_cffi_mul(self):
        for case in self.cases:
            matrix_l = case["l"]
            c_matrix_l = matrix_lib.create_matrix(
                matrix_l.shape[0], matrix_l.shape[1]
            )
            fill_matrix(c_matrix_l, matrix_l)

            matrix_r = case["r"]
            c_matrix_r = matrix_lib.create_matrix(
                matrix_r.shape[0], matrix_r.shape[1]
            )
            fill_matrix(c_matrix_r, matrix_r)

            result = matrix_l @ matrix_r
            c_result = matrix_lib.mul(c_matrix_l, c_matrix_r)
            c_result_list = ffi.unpack(
                c_result.data, c_result.rows * c_result.cols
            )
            self.assertListEqual(result.flatten().tolist(), c_result_list)

    def test_py_mul(self):
        for case in self.cases:
            matrix_l = case["l"]
            py_matrix_l = PyMatrix(
                matrix_l.shape[0], matrix_l.shape[1], matrix_l.flatten()
            )

            matrix_r = case["r"]
            py_matrix_r = PyMatrix(
                matrix_r.shape[0], matrix_r.shape[1], matrix_r.flatten()
            )

            result = matrix_l @ matrix_r
            py_result = matrix_mul(py_matrix_l, py_matrix_r)
            self.assertListEqual(result.reshape(-1).tolist(), py_result.data)
