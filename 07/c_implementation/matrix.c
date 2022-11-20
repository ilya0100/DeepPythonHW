#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "matrix.h"

#define EPS 1e-7


Matrix* create_matrix(size_t rows, size_t cols) {
    Matrix* new_matrix = malloc(sizeof(Matrix));
    if (new_matrix == NULL) {
        perror("Error: memory allocation error");
        return NULL;
    }
    if (rows < 1 || cols < 1) {
        perror("Error: the number of rows and columns should be >= 1");
        free(new_matrix);
        return NULL;
    }
    new_matrix->rows = rows;
    new_matrix->cols = cols;
    new_matrix->data = malloc(sizeof(double) * rows * cols);

    if (new_matrix->data == NULL) {
        perror("error");
        free(new_matrix);
        return NULL;
    }
    return new_matrix;
}

void free_matrix(Matrix* matrix) {
    if (matrix->data != NULL) {
        free(matrix->data);
    }
    if (matrix != NULL) {
        free(matrix);
    }
}

int get_elem(const Matrix* matrix, size_t row, size_t col, double* val) {
    if (matrix == NULL) {
        return -1;
    }
    if (matrix->data == NULL) {
        return -1;
    }
    if (row >= matrix->rows || col >= matrix->cols) {
        return -1;
    }
    *val = matrix->data[row * matrix->cols + col];
    return 0;
}

int set_elem(Matrix* matrix, size_t row, size_t col, double val) {
    if (matrix == NULL) {
        return -1;
    }
    if (matrix->data == NULL) {
        return -1;
    }
    if (row >= matrix->rows || col >= matrix->cols) {
        return -1;
    }
    matrix->data[row * matrix->cols + col] = val;
    return 0;
}

Matrix* mul(const Matrix* l, const Matrix* r) {
    if (l == NULL || r == NULL) {
        return NULL;
    }
    if (l->data == NULL || r->data == NULL) {
        return NULL;
    }
    if (l->cols != r->rows) {
        return NULL;
    }
    Matrix* mul_matrix = create_matrix(l->rows, r->cols);
    if (mul_matrix == NULL) {
        return NULL;
    }
    double buffer_l, buffer_r;

    for (size_t j = 0; j < r->cols; ++j) {
        for (size_t i = 0; i < l->rows; ++i) {
            double summ = 0;

            for (size_t k = 0; k < l->cols; ++k) {
                if (get_elem(l, i, k, &buffer_l) || get_elem(r, k, j, &buffer_r)) {
                    free_matrix(mul_matrix);
                    return NULL;
                }
                summ += buffer_l * buffer_r;
            }
            if (set_elem(mul_matrix, i, j, summ)) {
                free_matrix(mul_matrix);
                return NULL;
            }
        }
    }
    return mul_matrix;
}
