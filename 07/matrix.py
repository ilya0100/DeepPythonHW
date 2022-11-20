from dataclasses import dataclass


@dataclass
class PyMatrix:
    def __init__(self, rows, cols, source=None):
        if not source is None:
            source_size = len(source)
            if rows * cols != source_size:
                raise ValueError(
                    f"Cannot create mitrix with shape: ({rows}, {cols}) from source with len: {source_size}"
                )
        self.rows = rows
        self.cols = cols
        if not source is None:
            self.data = [float(i) for i in source]
        else:
            self.data = [0] * (rows * cols)

    def __getitem__(self, pos):
        return self.data[pos[0] * self.cols + pos[1]]

    def __setitem__(self, pos, value):
        self.data[pos[0] * self.cols + pos[1]] = value


def matrix_mul(lhs: PyMatrix, rhs: PyMatrix):
    if lhs.cols != rhs.rows:
        raise ValueError("Left matrix columns do not equal right matrix rows")
    matrix = PyMatrix(lhs.rows, rhs.cols)

    for j in range(rhs.cols):
        for i in range(lhs.rows):
            summ = 0.0

            for k in range(lhs.cols):
                summ += lhs[i, k] * rhs[k, j]
            matrix[i, j] = summ
    return matrix
