import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib.animation as animation
import time
import sys
from logging import FileHandler
import logging


def get_logger(name=__file__, file='log.txt', encoding='utf-8'):
    # фукнция логгирования
    
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Будут строки вида: "[2017-08-23 09:54:55,356] main.py:34 DEBUG    foo"
    # formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')
    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    # В файл
    fh = FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log


log = get_logger()

# КОНСТАНТЫ
velocity = 0
omega = 0
r = 0.5
circle_R = 3.5
a = 0.1  # ускорение

V_max = 2.5
omega_max = math.radians(V_max / r)

L = 1.2
teta = math.radians(0)
teta_max = math.radians(30)

# координаты базовой траектории (синей линии)
x_straight_begin = 0
y_straight_begin = 1

x_straight_finish = 50
y_straight_finish = 1

# координаты базовой круговой траектори
x_angle_begin = 50
y_angle_begin = 1

x_angle_finish = 50
y_angle_finish = 7

# погрешность для финишной точки ( диаметр окружности погрешности )
e = 0.6

# точность обработки (влияет на скорость обработки)
speed = 5

# стартовые данные робота
fi_i_start = math.radians(0)  # азимут (градусы в скобках)
x_i_start = 10
y_i_start = -5


g_count = 0

plt.style.use('seaborn')

# fig, ax = plt.subplots()
fig = plt.figure()
ax1 = fig.add_subplot()

xs = []
ys = []


def animate(x, y, x_predicted, y_predicted, omega, theta, velocity, fi, w_left, w_right, circle_R=3.5):
    xs.append(x)
    ys.append(y)
    a, b = 23.75 * 0.2, 23.67 * 0.2

    ax1.clear()
    plt.scatter(x_predicted, y_predicted, color='green', s=20, zorder=10)
    plt.plot([x_straight_begin, x_straight_finish - 0.45], [y_straight_begin, y_straight_finish],
             color='cornflowerblue', linewidth=4)
    plt.plot([x_straight_finish - 0.5, -0.76], [5.76, 5.76], color='cornflowerblue', linewidth=4)
    ax1.add_patch(Arc((49.5, 3.38), a, b,
                      theta1=271.0, theta2=449.0, edgecolor='cornflowerblue', lw=4))
    ax1.add_patch(Arc((-0.55, 3.4), a, b,
                      theta1=90.0, theta2=180.0, edgecolor='cornflowerblue', lw=4))
    plt.plot([-2.9, -2.9], [3.39, 12], color='cornflowerblue', linewidth=4)

    ax1.add_patch(Arc((-0.5, 12), a, b,
                      theta1=180.0, theta2=270.0, edgecolor='cornflowerblue', lw=4))
    plt.plot([-0.65, x_straight_finish], [9.645, 9.645], color='cornflowerblue', linewidth=4)
    plt.xlim(-6, 56)
    plt.ylim(-12, 17)
    plt.gca().set_aspect('equal', adjustable='box')
    ax1.plot(xs, ys, color='red', linewidth=2)

    if math.sin(theta) == 0:
        radius = 0
    else:
        radius = L / math.sin(theta)

    log.debug('Угол поворота передних колес: ' + str(
        round(math.degrees(theta), 2)) + 'град. ' + '\n' + 'Угловая скорость ведущих колес: ' + str(
        round(math.degrees(math.degrees(omega)), 2)) + 'град./с ' +
              '\n' + 'Скорость: ' + str(round(velocity, 2)) + ' м/с' + '    |    ' + 'Радиус разворота: ' + str(
        round(radius, 2)) + ' м' + '\n' + 'X: ' + str(round(x, 2)) + ' м' + '    |    ' + 'Y: ' + str(
        round(y, 2)) + ' м' + '    |    ' + 'Азимут: ' + str(round(math.degrees(fi), 2)) + ' град.')

    plt.text(31, -6, 'Угол поворота передних колес: ' + str(round(math.degrees(theta), 2)) + ' град.', size='medium',
             family='fantasy')
    plt.text(31, -7, 'Угловая скорость ведущих колес: ' + str(round(math.degrees(math.degrees(omega)), 2)) + ' град/с',
             size='medium', family='fantasy')
    plt.text(31, -8, 'Скорость: ' + str(round(velocity, 2)) + ' м/с' + '    |    ' + 'Радиус разворота: ' + str(
        round(radius, 2)) + ' м', size='medium', family='fantasy')
    plt.text(31, -9, 'X: ' + str(round(x, 2)) + ' м' + '    |    ' + 'Y: ' + str(
        round(y, 2)) + ' м' + '    |    ' + 'Азимут: ' + str(round(math.degrees(fi), 2)) + ' град.', size='medium',
             family='fantasy')
    plt.text(31, -10, 'Левое колесо: ' + str(
        round(math.degrees(math.degrees(w_left)), 2)) + ' м/с' + '    |    ' + 'Правое колесо: ' + str(
        round(math.degrees(math.degrees(w_right)), 2)) + ' м/с', size='medium', family='fantasy')

    plt.title('Работа функции управления роботом')
    plt.pause(0.0003)


def straight(x_i, y_i, fi_i, teta, g_count, x_finish, y_finish, x_begin, y_begin, time, velocity):
    # функция движения по прямой
    
    var = 30

    while math.sqrt(((x_finish - x_i) ** 2 + (y_finish - y_i) ** 2)) >= e:
        fi_predict_i = fi_i
        x_predict = x_i
        y_predict = y_i

        d = ((y_finish - y_begin) * x_predict - (
                x_finish - x_begin) * y_predict + x_finish * y_begin - y_finish * x_begin) / (
                math.sqrt((y_finish - y_begin) ** 2 + (x_finish - x_begin) ** 2))

        if abs(d) > 5:
            corrected = straight(x_predict, y_predict, fi_predict_i, teta, g_count,
                                      x_begin, y_begin, x_i, y_i, 1, velocity)
            x_i = corrected[0]
            y_i = corrected[1]
            fi_i = corrected[2]

            fi_predict_i = fi_i
            x_predict = x_i
            y_predict = y_i
        
        if 3 > abs(d) > 1:
           var = 50
        else:
           var = 30

        # разгон и торможение
        distance = math.sqrt((x_i - x_finish) ** 2 + (y_i + y_finish) ** 2)
        S = velocity ** 2 / 2 * a

        if distance > S:
            if V_max - a < velocity <= V_max:
                velocity = V_max
            else:
                velocity += a
        else:
            if velocity > 0:
                velocity -= a
            else:
                velocity = 0

        omega = math.radians(velocity / r)

        for i in range(0, var):
            '''
            В этом цикле обрабатывается предиктивная координата
            то есть просчитывается, дэ наш робот будет через определенное
            количество шагов. Количество шагов задается ренжой цикла. 
            '''

            fi_predict = omega * r * math.sin(teta) / L
            fi_predict_i += fi_predict
            x_predict_add = omega * r * math.cos(fi_predict_i)
            y_predict_add = omega * r * math.sin(fi_predict_i)

            x_predict += x_predict_add
            y_predict += y_predict_add


        d = ((y_finish - y_begin) * x_predict - (
                x_finish - x_begin) * y_predict + x_finish * y_begin - y_finish * x_begin) / (
                math.sqrt((y_finish - y_begin) ** 2 + (x_finish - x_begin) ** 2))


        delta_teta = teta_max * math.tanh(d)

        w_left, w_right = diff(omega, teta, delta_teta)

        teta += delta_teta

        if teta > teta_max and teta > 0:
            teta = math.radians(30)

        if teta < -teta_max and teta < 0:
            teta = math.radians(-30)

        fi_add = omega * r * math.sin(teta) * (1 / L)
        fi_i += fi_add
        x_add = omega * r * math.cos(fi_i)
        y_add = omega * r * math.sin(fi_i)

        x_i += x_add
        y_i += y_add


        if g_count == speed:
            
            animate(x_i, y_i, x_predict, y_predict, omega, teta, velocity, fi_i, w_left, w_right)
            g_count = 0
        else:
            g_count += 1

    return x_i, y_i, fi_i


def angle(x_i, y_i, fi_i_start, teta, g_count, x_finish, y_finish, x_begin, y_begin, time, fi_turn, velocity, omega):
    # функция движения по дуге
    
    fi_i = fi_i_start
    fi_i_finish = math.degrees(fi_i_start) + fi_turn

    while math.degrees(fi_i) <= fi_i_finish:
        fi_predict_i = fi_i
        x_predict = x_i
        y_predict = y_i
        if 3 > abs(y_i - y_finish) > 1:
            var = 40
        elif abs(y_i - y_finish) >= 3:
            var = 60
        else:
            var = 20

        #  Разгон и торможение
        P = math.acos(1 - ((x_i - x_finish) ** 2 + (y_i - y_finish) ** 2) / (2 * circle_R ** 2)) * circle_R
        S = velocity ** 2 / 2 * a

        if P > S:
            if V_max - a < velocity <= V_max:
                velocity = V_max
                omega = omega_max
            else:
                velocity += a
                omega += math.radians(a / r)
        else:
            velocity -= a
            omega -= math.radians(a / r)

        for i in range(0, var):
            '''
            В этом цикле обрабатывается предиктивная координата
            то есть просчитывается, дэ наш робот будет через определенное
            количество шагов. Количество шагов задается ренжой цикла. 
            '''

            fi_predict = omega * r * math.sin(teta) / L
            fi_predict_i += fi_predict
            x_predict_add = omega * r * math.cos(fi_predict_i)
            y_predict_add = omega * r * math.sin(fi_predict_i)

            x_predict += x_predict_add
            y_predict += y_predict_add

        

        d = math.sqrt(
            (x_predict - x_straight_finish) ** 2 + (y_predict - (y_straight_finish - circle_R)) ** 2) - circle_R

        delta_teta = math.asin(L / circle_R)
        w_left, w_right = diff(omega, teta, delta_teta)

        teta += delta_teta

        if teta > teta_max and teta > 0:
            teta = math.radians(30)

        if teta < -teta_max and teta < 0:
            teta = math.radians(-30)

        fi_add = omega * r * math.sin(teta) * (1 / L)
        fi_i += fi_add
        x_add = omega * r * math.cos(fi_i)
        y_add = omega * r * math.sin(fi_i)

        x_i += x_add
        y_i += y_add


        if g_count == speed:
            animate(x_i, y_i, x_predict, y_predict, omega, teta, velocity, fi_i, w_left, w_right)
            g_count = 0
        else:
            g_count += 1


    return x_i, y_i, fi_i


def diff(omega, theta, delta_theta):
    """
    param:
    omega - угловая скорость
    theta - угол поворота колес
    delta_theta - угол необходимого доворота

    return:
    omega_left - угловая скорость левого колеса
    omega_right - угловая скорость правого колеса
    """
    omega_left = omega * (1 + omega / L * math.sin(theta + delta_theta))
    omega_right = omega * (1 - omega / L * math.sin(theta + delta_theta))

    return omega_left, omega_right


# до первого разворота
coords = straight(x_i_start, y_i_start, fi_i_start, teta, g_count,
                  x_straight_finish, y_straight_finish, x_straight_begin, y_straight_begin, 0, velocity)

# первый разворот
angle_coords = angle(coords[0], coords[1], coords[2], teta, g_count,
                     x_angle_finish, y_angle_finish, x_angle_begin, y_angle_begin, 0, 180, velocity, omega)

x_straight_finish_2 = -0.5
y_straight_finish_2 = angle_coords[1]

# после второго разворота
coords_2 = straight(angle_coords[0], angle_coords[1], angle_coords[2], teta, g_count, x_straight_finish_2,
                      y_straight_finish_2, angle_coords[0], angle_coords[1], 0, velocity)

x_angle_finish_2 = -2
y_angle_finish_2 = 3.35
x_angle_begin = x_straight_finish_2
y_angle_begin = y_straight_finish_2

# выезжаем на траекторию для разворота задом
angle_coords_2 = angle(x_angle_begin, y_angle_begin, coords_2[2], teta, g_count,
                       x_angle_finish_2, y_angle_finish_2, x_angle_begin, y_angle_begin, 0, 90, velocity, omega)

x_straight_finish_3 = angle_coords_2[0]
y_straight_finish_3 = 12

# едем по прямой задом
coords_3 = straight(angle_coords_2[0], angle_coords_2[1], math.radians(90), teta, g_count,
                    x_straight_finish_3, y_straight_finish_3, angle_coords_2[0], angle_coords_2[1], 0, velocity)

x_angle_finish_3 = -0.65
y_angle_finish_3 = 9.645
x_angle_begin = x_straight_finish_3
y_angle_begin = y_straight_finish_3

# выезжаем на траекторию движения прямо вдоль ряда
angle_coords_3 = angle(x_angle_begin, y_angle_begin, math.radians(270), teta, g_count,
                       x_angle_finish_3, y_angle_finish_3, x_angle_begin, y_angle_begin, 0, 90, velocity, omega)

x_straight_finish_4 = 50
y_straight_finish_4 = angle_coords_3[1]

# прямое движение вдоль ряда
coords_5 = straight(angle_coords_3[0], angle_coords_3[1], angle_coords_3[2], teta, g_count,
                    x_straight_finish_4, y_straight_finish_4, angle_coords_3[0], angle_coords_3[1], 0, velocity)

plt.show()
