import subprocess  # для запуска shell-команд
import os  # для удаления файлов


def main():
    # Собираем требования к матрицам
    matrix_size = int(input("Введите размер квадратной матрицы: "))
    min_value = int(input("Введите минимальное значение для элементов матрицы: "))
    max_value = int(input("Введите максимальное значение для элементов матрицы: "))
    generate_floats = input("Генерировать float значения? (y/n): ")

    # Запускаем модуль Matrix_generator.py
    subprocess.run(["..\\venv\\Scripts\\python.exe", "input\\Matrix_generator.py", str(matrix_size), str(min_value),
                    str(max_value), str(generate_floats)], check=True)

    num_executions = int(input("Введите количество тестовых запусков: "))

    if generate_floats != "y":
        use_bigint = input("Хотите использовать BigInt значения? (y/n): ")
    else:
        use_bigint = "n"

    while True:
        num_threads = input("Введите желаемое количество потоков (от 1 до 32): ")
        if 1 <= int(num_threads) <= 32:
            break
        else:
            print("Пожалуйста, введите число от 1 до 32.")

    # Запускаем модуль TestPlatform.py
    subprocess.run(
        ["..\\venv\\Scripts\\python.exe", "TestPlatform.py", str(num_executions), str(generate_floats), str(use_bigint),
         str(num_threads)], check=True)

    # Удаляем матрицы для возможности перезапуска приложения
    temp_dir = "temp"
    for file_name in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file_name))


if __name__ == "__main__":
    main()
