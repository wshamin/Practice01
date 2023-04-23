import math

def request_user_input():
    d1 = float(input("Введите кратчайшее расстояние от спасателя до кромки воды, d1 (в ярдах): "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, d2 (в футах): "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (в ярдах): "))
    v_sand = float(input("Введите скорость движения спасателя по песку, v_sand (в милях в час): "))
    n = float(input("Введите коэффициент замедления спасателя при движении в воде, n: "))
    theta1 = float(input("Введите направление движения спасателя по песку, theta1 (в градусах): "))

    return d1, d2, h, v_sand, n, theta1

def make_calculations(d1, d2, h, v_sand, n, theta1):
    d1_feet = d1 * 3
    h_feet = h * 3
    v_sand_fps = v_sand * 5280 / 3600
    theta1_radians = math.radians(theta1)

    x = d1_feet * math.tan(theta1_radians)
    L1 = math.sqrt(x ** 2 + d1_feet ** 2)
    L2 = math.sqrt((h_feet - x) ** 2 + d2 ** 2)

    t = (1 / v_sand_fps) * (L1 + n * L2)

    return theta1, t

d1, d2, h, v_sand, n, theta1 = request_user_input()
theta1, t = make_calculations(d1, d2, h, v_sand, n, theta1)

print(f"Если спасатель начнёт движение под углом theta1, равным {int(theta1)} градусам, "
      f"он достигнет утопающего через {t:.1f} секунды")