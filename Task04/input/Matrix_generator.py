import numpy as np
import pandas as pd
import argparse  # Парсер аргументов для запуска


def generate_matrix(rows, cols, min_val, max_val, float_values=False):
    if float_values:
        matrix = np.random.uniform(min_val, max_val, (rows, cols))
    else:
        matrix = np.random.uniform(min_val, max_val, (rows, cols))
        matrix = matrix.astype("int64")
    return matrix


def save_matrix_to_csv(matrix, file_name):
    df = pd.DataFrame(matrix)
    df.to_csv(file_name, index=False, header=False)


def main():
    # Добавляем аргументы командной строки
    parser = argparse.ArgumentParser(description="Параметры для матриц")
    parser.add_argument("matrix_size", type=int, help="Размер квадратной матрицы")
    parser.add_argument("min_value", type=int, help="Минимальное значение для элементов матрицы")
    parser.add_argument("max_value", type=int, help="Максимальное значение для элементов матрицы")
    parser.add_argument("generate_floats", type=str, help="Генерировать ли float значения")
    args = parser.parse_args()

    # Вытаскиваем параметры запуска из парсера
    matrix_size = args.matrix_size
    min_value = args.min_value
    max_value = args.max_value
    generate_floats = args.generate_floats == 'y'

    matrix_a = generate_matrix(matrix_size, matrix_size, min_value, max_value, generate_floats)
    matrix_b = generate_matrix(matrix_size, matrix_size, min_value, max_value, generate_floats)

    save_matrix_to_csv(matrix_a, "temp\\matrix_a.csv")
    save_matrix_to_csv(matrix_b, "temp\\matrix_b.csv")

    print("Матрицы А и Б были созданы и сохранены в matrix_a.csv и matrix_b.csv")


if __name__ == "__main__":
    main()
