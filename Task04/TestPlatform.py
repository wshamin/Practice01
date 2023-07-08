import subprocess  # Библиотека для запуска новых процессов, подключения к их вводу/выводу/ошибкам и их завершения
import time  # Библиотека для работы со временем
import matplotlib.pyplot as plt  # Библиотека для создания статических, анимированных и интерактивных визуализаций в Python
import numpy as np  # Библиотека для работы с массивами и матрицами
import argparse # Парсер аргументов для запуска
import webbrowser # для открытия изображения

# Функция запуска программы DGEMM определенное количество раз, с замером времени выполнения каждого запуска
def run_dgemm(command, num_executions):
    exec_times = []  # Список, хранящий время выполнения каждого запуска
    for _ in range(num_executions):  # Запускаем программу num_executions раз
        start_time = time.time()  # Запоминаем время начала
        subprocess.run(command, check=True)  # Запускаем программу
        end_time = time.time()  # Запоминаем время окончания
        exec_times.append(end_time - start_time)  # Рассчитываем время выполнения и добавляем в список
    return exec_times  # Возвращаем список времени выполнения каждого запуска

# Функция для создания графиков и расчета статистических данных по времени выполнения программ
def plot_stats(exec_times, filename, data_type):
    languages = ["Java", "CSharp", "Python"]  # Список языков программирования
    colors = ["b", "r", "g"]  # Список цветов для графиков

    plt.figure(figsize=(12, 7))  # Создание новой фигуры

    # Построение графиков для каждого языка программирования
    for i in range(3):
        plt.plot(exec_times[i], color=colors[i], label=languages[i], linewidth=1)

    plt.legend(loc="upper right")  # Добавление легенды на график
    plt.xlabel("Количество запусков")  # Подпись оси x
    plt.ylabel("Время выполнения (сек.)")  # Подпись оси y
    plt.title(f"t выполнения DGEMM на Java, C# и Python для {data_type}")  # Заголовок графика. f-string используется для вставки data_type в строку

    stats_text = ""  # Текст с расчетными статистическими данными

    # Расчет и формирование статистических данных по времени выполнения для каждого языка программирования
    for i in range(3):
        t_min = min(exec_times[i])  # Минимальное время
        t_max = max(exec_times[i])  # Максимальное время
        t_avg = sum(exec_times[i]) / len(exec_times[i])  # Среднее время
        t_std = np.std(exec_times[i])  # Стандартное отклонение
        t_med = np.median(exec_times[i])  # Медиана

        stats_text += r"$\bf{" + languages[i] + "}$" + ":\n"  # Название языка
        stats_text += f"tMin = {t_min:.2f} s\n"  # Минимальное время
        stats_text += f"tMax = {t_max:.2f} s\n"  # Максимальное время
        stats_text += f"tAvg = {t_avg:.2f} s\n"  # Среднее время
        stats_text += f"tStd = {t_std:.2f} s\n"  # Стандартное отклонение
        stats_text += f"tMed = {t_med:.2f} s\n\n"  # Медиана

    plt.figtext(0.1, 0.02, stats_text, fontsize=10)  # Добавление текста со статистическими данными на график

    plt.subplots_adjust(left=0.3)  # Регулировка местоположения графика на фигуре

    plt.savefig(filename)  # Сохранение графика в файл

# Главная функция
def main():
    # Добавляем аргументы командной строки
    parser = argparse.ArgumentParser(description="Параметры для DGEMM тестов")
    parser.add_argument("num_executions", type=int, help="Количество тестировочных запусков")
    parser.add_argument("generate_floats", type=str, help="Используем ли float (y/n)")
    parser.add_argument("use_bigint", type=str, help="Используем ли BigInt (y/n)")
    parser.add_argument("num_threads", type=int, help="Желаемое количество потоков (1-32)")
    args = parser.parse_args()

    # Вытаскиваем параметры запуска из парсера
    program_run_count = args.num_executions
    desired_datatype = "y" if args.generate_floats.lower() in ["y", "true"] else "n"
    desired_bigint = "y" if args.use_bigint.lower() in ["y", "true"] else "n"
    thread_count = args.num_threads

    exec_times = []  # Список, хранящий время выполнения каждого запуска для каждого языка программирования
    data_type = ""  # Переменная для хранения типа данных

    # Условия для определения типа данных и компиляции/сборки соответствующих программ
    if desired_datatype == "y":  # Если пользователь выбрал использование типа данных Float
        data_type = "Float"  # Устанавливаем тип данных
        # Компилируем/собираем программы с использованием типа данных Float
        subprocess.run(["javac.exe", "-d", "out\\production\\Task04", "DGEMM\\Java\\DGEMM_Java_Primitive_Float.java"], check=True)
        subprocess.run(["dotnet", "build", "DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Float\\DGEMM_CSharp_Primitive_Float.csproj"], check=True)
        # Список команд для запуска программ
        programs = [["java", "-cp", "out\\production\\Task04", "DGEMM_Java_Primitive_Float", "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_Java_Float_result.csv", str(thread_count)],
                    ["DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Float\\bin\\Debug\\net8.0\\DGEMM_CSharp_Primitive_Float.exe", "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_CSharp_Primitive_Float_result.csv", str(thread_count)],
                    ["..\\venv\\Scripts\\python.exe", "DGEMM\\Python\\DGEMM_Python_Float.py", "--a", "temp\\matrix_a.csv", "--b", "temp\\matrix_b.csv", "--o", "DGEMM\\output\\DGEMM_Python_Float_result.csv", "--t", str(thread_count)]]
    elif desired_bigint == "y":  # Если пользователь выбрал использование типа данных BigInteger
        data_type = "BigInteger"  # Устанавливаем тип данных
        # Компилируем/собираем программы с использованием типа данных BigInteger
        subprocess.run(["javac.exe", "-d", "out\\production\\Task04", "DGEMM\\Java\\DGEMM_Java_BigInteger.java"], check=True)
        subprocess.run(["dotnet", "build", "DGEMM\\CSharp\\DGEMM_CSharp_BigInteger\\DGEMM_CSharp_BigInteger.csproj"], check=True)
        # Список команд для запуска программ
        programs = [["java", "-cp", "out\\production\\Task04", "DGEMM_Java_BigInteger", "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_Java_BigInteger_result.csv", str(thread_count)],
                    ["DGEMM\\CSharp\\DGEMM_CSharp_BigInteger\\bin\\Debug\\net8.0\\DGEMM_CSharp_BigInteger.exe", "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_CSharp_BigInteger_result.csv", str(thread_count)],
                    ["..\\venv\\Scripts\\python.exe", "DGEMM\\Python\\DGEMM_Python_Int.py", "--a", "temp\\matrix_a.csv", "--b", "temp\\matrix_b.csv", "--o", "DGEMM\\output\\DGEMM_Python_BigInt_result.csv", "--t", str(thread_count)]]
    else:  # Если пользователь выбрал использование типа данных Integer
        data_type = "Integer"  # Устанавливаем тип данных
        # Компилируем/собираем программы с использованием типа данных Integer
        subprocess.run(["javac.exe", "-d", "out\\production\\Task04", "DGEMM\\Java\\DGEMM_Java_Primitive_Int.java"], check=True)
        subprocess.run(["dotnet", "build", "DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Int\\DGEMM_CSharp_Primitive_Int.csproj"], check=True)
        # Список команд для запуска программ
        programs = [["java", "-cp", "out\\production\\Task04", "DGEMM_Java_Primitive_Int", "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_Java_Primitive_Int_result.csv", str(thread_count)],
                    ["DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Int\\bin\\Debug\\net8.0\\DGEMM_CSharp_Primitive_Int.exe", "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_CSharp_Primitive_Int_result.csv", str(thread_count)],
                    ["..\\venv\\Scripts\\python.exe", "DGEMM\\Python\\DGEMM_Python_Int.py", "--a", "temp\\matrix_a.csv", "--b", "temp\\matrix_b.csv", "--o", "DGEMM\\output\\DGEMM_Python_Int_result.csv", "--t", str(thread_count)]]
    # Запускаем каждую программу заданное количество раз и замеряем время выполнения
    for program in programs:
        exec_times.append(run_dgemm(program, program_run_count))

    # Рисуем график, сохраняем в файл, открываем
    image_path = f"DGEMM_{data_type}_Performance.png"
    plot_stats(exec_times, image_path, data_type)
    webbrowser.open(image_path)


if __name__ == "__main__":
    main()



