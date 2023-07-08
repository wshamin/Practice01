import numpy as np
import argparse
import multiprocessing as mp
import os


def load_matrix(filename):
    return np.loadtxt(filename, delimiter=',', dtype=np.int64)


def save_matrix(matrix, filename):
    np.savetxt(filename, matrix, delimiter=' ', fmt='%d')


def multiply_rows(args):
    matrix_a_row, matrix_b = args
    return np.dot(matrix_a_row, matrix_b)


def dgemm(matrix_a, matrix_b, num_threads):
    with mp.Pool(processes=num_threads) as pool:
        result_matrix = pool.map(multiply_rows, [(matrix_a[i], matrix_b) for i in range(matrix_a.shape[0])])
    return np.array(result_matrix, dtype=int)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a")
    parser.add_argument("--b")
    parser.add_argument("--o")
    parser.add_argument("--t", type=int, default=os.cpu_count())
    args = parser.parse_args()

    matrix_a = load_matrix(args.a)
    matrix_b = load_matrix(args.b)

    result_matrix = dgemm(matrix_a, matrix_b, args.t)
    save_matrix(result_matrix, args.o)


if __name__ == "__main__":
    main()
