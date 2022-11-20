typedef struct Matrix {
    size_t rows;
    size_t cols;
    double* data;
} Matrix;

Matrix* create_matrix(size_t rows, size_t cols);
void free_matrix(Matrix* matrix);

int get_elem(const Matrix* matrix, size_t row, size_t col, double* val);
int set_elem(Matrix* matrix, size_t row, size_t col, double val);

Matrix* mul(const Matrix* l, const Matrix* r);
