import subprocess  # Библиотека для запуска новых процессов
import time  # Библиотека для работы со временем
import matplotlib.pyplot as plt  # Библиотека для создания визуализаций в Python
import numpy as np  # Библиотека для работы с матрицами
import argparse  # Модуль для работы с аргументами
import webbrowser  # Библиотека для открытия изображения


# Функция запуска программы DGEMM определенное количество раз, с замером времени выполнения каждого запуска


def run_dgemm(command, num_executions):
    exec_times = []  # Список, хранящий время выполнения каждого запуска
    for _ in range(num_executions):
        start_time = time.time()
        subprocess.run(command, check=True)  # Запускаем программу
        end_time = time.time()
        exec_times.append(end_time - start_time)  # Рассчитываем время выполнения и добавляем в список
    return exec_times

# Функция для создания графиков и расчета статистики по времени выполнения программ


def plot_stats(exec_times, filename, data_type):
    languages = ["Java", "CSharp", "Python"]
    colors = ["b", "r", "g"]

    plt.figure(figsize=(12, 7))

    # Построение графиков для каждого языка программирования
    for i in range(3):
        plt.plot(exec_times[i], color=colors[i], label=languages[i], linewidth=1)

    plt.legend(loc="upper right")
    plt.xlabel("Количество запусков")
    plt.ylabel("Время выполнения (сек.)")
    plt.title(f"t выполнения DGEMM на Java, C# и Python для {data_type}")

    stats_text = ""

    # Расчет и запись статистики по времени выполнения для каждого языка программирования
    for i in range(3):
        t_min = min(exec_times[i])
        t_max = max(exec_times[i])
        t_avg = sum(exec_times[i]) / len(exec_times[i])
        t_std = np.std(exec_times[i])
        t_med = np.median(exec_times[i])

        stats_text += r"$\bf{" + languages[i] + "}$" + ":\n"
        stats_text += f"tMin = {t_min:.2f} s\n"
        stats_text += f"tMax = {t_max:.2f} s\n"
        stats_text += f"tAvg = {t_avg:.2f} s\n"
        stats_text += f"tStd = {t_std:.2f} s\n"
        stats_text += f"tMed = {t_med:.2f} s\n\n"

    plt.figtext(0.1, 0.02, stats_text, fontsize=10)

    plt.subplots_adjust(left=0.3)  # Регулировка местоположения графика на фигуре

    plt.savefig(filename)  # Сохранение графика в файл


def main():
    # Добавляем аргументы командной строки
    parser = argparse.ArgumentParser(description="Параметры для DGEMM тестов")
    parser.add_argument("num_executions", type=int, help="Количество тестовых запусков")
    parser.add_argument("generate_floats", type=str, help="Используем ли float (y/n)")
    parser.add_argument("use_bigint", type=str, help="Используем ли BigInt (y/n)")
    parser.add_argument("num_threads", type=int, help="Желаемое количество потоков (1-32)")
    args = parser.parse_args()

    # Вытаскиваем параметры запуска из парсера
    program_run_count = args.num_executions
    desired_datatype = "y" if args.generate_floats.lower() in ["y", "true"] else "n"
    desired_bigint = "y" if args.use_bigint.lower() in ["y", "true"] else "n"
    thread_count = args.num_threads

    exec_times = []
    data_type = ""

    # Условия для определения типа данных и компиляции/сборки соответствующих программ
    if desired_datatype == "y":
        data_type = "Float"
        subprocess.run(["javac.exe", "-d", "out\\production\\Task04", "DGEMM\\Java\\DGEMM_Java_Primitive_Float.java"],
                       check=True)
        subprocess.run(["dotnet", "build",
                        "DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Float\\DGEMM_CSharp_Primitive_Float.csproj"], check=True)
        programs = [["java", "-cp", "out\\production\\Task04", "DGEMM_Java_Primitive_Float", "temp\\matrix_a.csv",
                     "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_Java_Float_result.csv", str(thread_count)],
                    ["DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Float\\bin\\Debug\\net8.0\\DGEMM_CSharp_Primitive_Float.exe",
                     "temp\\matrix_a.csv", "temp\\matrix_b.csv",
                     "DGEMM\\output\\DGEMM_CSharp_Primitive_Float_result.csv", str(thread_count)],
                    ["..\\venv\\Scripts\\python.exe", "DGEMM\\Python\\DGEMM_Python_Float.py", "--a",
                     "temp\\matrix_a.csv", "--b", "temp\\matrix_b.csv", "--o",
                     "DGEMM\\output\\DGEMM_Python_Float_result.csv", "--t", str(thread_count)]]
    elif desired_bigint == "y":
        data_type = "BigInteger"
        subprocess.run(["javac.exe", "-d", "out\\production\\Task04", "DGEMM\\Java\\DGEMM_Java_BigInteger.java"],
                       check=True)
        subprocess.run(["dotnet", "build", "DGEMM\\CSharp\\DGEMM_CSharp_BigInteger\\DGEMM_CSharp_BigInteger.csproj"],
                       check=True)
        programs = [["java", "-cp", "out\\production\\Task04", "DGEMM_Java_BigInteger", "temp\\matrix_a.csv",
                     "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_Java_BigInteger_result.csv", str(thread_count)],
                    ["DGEMM\\CSharp\\DGEMM_CSharp_BigInteger\\bin\\Debug\\net8.0\\DGEMM_CSharp_BigInteger.exe",
                     "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_CSharp_BigInteger_result.csv",
                     str(thread_count)],
                    ["..\\venv\\Scripts\\python.exe", "DGEMM\\Python\\DGEMM_Python_Int.py", "--a", "temp\\matrix_a.csv",
                     "--b", "temp\\matrix_b.csv", "--o", "DGEMM\\output\\DGEMM_Python_BigInt_result.csv", "--t",
                     str(thread_count)]]
    else:
        data_type = "Integer"
        subprocess.run(["javac.exe", "-d", "out\\production\\Task04", "DGEMM\\Java\\DGEMM_Java_Primitive_Int.java"],
                       check=True)
        subprocess.run(["dotnet", "build",
                        "DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Int\\DGEMM_CSharp_Primitive_Int.csproj"], check=True)
        programs = [["java", "-cp", "out\\production\\Task04", "DGEMM_Java_Primitive_Int", "temp\\matrix_a.csv",
                     "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_Java_Primitive_Int_result.csv", str(thread_count)],
                    ["DGEMM\\CSharp\\DGEMM_CSharp_Primitive_Int\\bin\\Debug\\net8.0\\DGEMM_CSharp_Primitive_Int.exe",
                     "temp\\matrix_a.csv", "temp\\matrix_b.csv", "DGEMM\\output\\DGEMM_CSharp_Primitive_Int_result.csv",
                     str(thread_count)],
                    ["..\\venv\\Scripts\\python.exe", "DGEMM\\Python\\DGEMM_Python_Int.py", "--a", "temp\\matrix_a.csv",
                     "--b", "temp\\matrix_b.csv", "--o", "DGEMM\\output\\DGEMM_Python_Int_result.csv", "--t",
                     str(thread_count)]]

    for program in programs:
        exec_times.append(run_dgemm(program, program_run_count))

    # Рисуем график, сохраняем в файл, открываем
    image_path = f"DGEMM_{data_type}_Performance.png"
    plot_stats(exec_times, image_path, data_type)
    webbrowser.open(image_path)


if __name__ == "__main__":
    main()
