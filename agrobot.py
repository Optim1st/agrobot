import math
from pySerialTransfer import pySerialTransfer as txfer
import matplotlib.pyplot as plt
import time

### Константы ###
x_begin = 0  # начальная координата x
y_begin = 0  # начальная координата y
wheel_angle = 0
length_vehicle = 2  # длина робота
link = txfer.SerialTransfer('COM9', 115200, debug=True)
link.open()
R = 5.25  # радиус окружности
rcved_turn = 0 # полученный угол поворота с ардуино
send_size = 0

velocity = 0  # скорость

fi_angle_begin = 0  # начальный азимут
fi_angle = 0

req_x_num = 100
req_y_num = 120
### ОСНОВНОЙ ПОТОК ###
x_end = 0
y_end = 0


def angle_direction(R, fi_angle_begin, x_begin, y_begin, req_angle, dir_turn):
    d_begin = 0
    direction = 1


    #wheel_angle = math.asin(length_vehicle / R)  # находим угол поворота колеса (тета)
    wheel_angle = math.radians(30) # фиксированный угол поворота


    while fi_angle_begin < req_angle:
        # плавный старт
        if d_begin < math.pi:
            d_begin = d_begin + math.pi / 10
            velocity = velocity + math.sin(d_begin)
        velocity = velocity * 1.3

        while not link.available():
            pass
        rcved_turn = link.rx_obj(obj_type=list,
                                 obj_byte_size=2, list_format='h')
        if rcved_turn[0] < 700:
            turn_go = 1
            dir_turn = 0
            print(velocity, direction, turn_go, dir_turn, 'довернули', rcved_turn[0])
            list_ = [velocity, direction, turn_go, dir_turn]

        fi_angle_add = (velocity / length_vehicle) * math.sin(wheel_angle)  # находим угол прирощения

        fi_angle = fi_angle_begin + fi_angle_add  # находим конечный азимут

        x_add = velocity * math.cos(math.radians(fi_angle))  # находим координату X прирощения
        y_add = velocity * math.sin(math.radians(fi_angle))  # находим координату Y прирощения

        x_begin += x_add  # находим конечную координату X
        y_begin += y_add  # находим конечную координату Y

        fi_angle_begin = fi_angle

        print(velocity, direction, turn_go, dir_turn, 'разворот', rcved_turn[0])
        list_ = [velocity, direction, turn_go, dir_turn]
        list_size = link.tx_obj(list_)
        send_size = list_size
        link.send(send_size)
        time.sleep(0.25)

        
    return x_begin, y_begin, fi_angle_begin


def test_func(req_x_num, req_y_num, fi_angle, x_begin, y_begin):
    velocity = 0
    d_begin = 0
    send_size = 0
    direction = 1
    dir_turn = 0
    turn_go = 0
    while (x_begin < req_x_num) or (y_begin < req_y_num):
        #плавный старт
        if d_begin < math.pi:
            d_begin = d_begin + math.pi/10
            velocity = velocity + math.sin(d_begin)

        x_add = velocity * math.cos(fi_angle)  # находим координату X прирощения
        y_add = velocity * math.sin(fi_angle)  # находим координату Y прирощения

        x_begin += x_add  # находим конечную координату X
        y_begin += y_add  # находим конечную координату Y
        print(velocity, direction, turn_go, dir_turn, 'прямо')
        list_ = [velocity, direction, turn_go, dir_turn]
        list_size = link.tx_obj(list_)
        send_size = list_size
        link.send(send_size)
        time.sleep(0.5)
    return x_begin, y_begin


def test_func_2(req_x_num, req_y_num, fi_angle, x_begin, y_begin):
    velocity = 0
    d_begin = 0
    send_size = 0
    direction = 1
    dir_turn = 0
    turn_go = 0
    while (x_begin > req_x_num) or (y_begin > req_y_num):
        #плавный старт
        if d_begin < math.pi:
            d_begin = d_begin + math.pi/10
            velocity = velocity + math.sin(d_begin)

        x_add = velocity * math.cos(fi_angle)  # находим координату X прирощения
        y_add = velocity * math.sin(fi_angle)  # находим координату Y прирощения

        x_begin += x_add  # находим конечную координату X
        y_begin += y_add  # находим конечную координату Y
        print(velocity, direction, turn_go, dir_turn, 'другое прямо')
        list_ = [velocity, direction, turn_go, dir_turn]
        list_size = link.tx_obj(list_)
        send_size = list_size
        link.send(send_size)
        time.sleep(0.4)

    return x_begin, y_begin

def test_func_backward(req_x_num, req_y_num, fi_angle, x_begin, y_begin):
    velocity = 0
    d_begin = 0
    send_size = 0
    direction = 0
    dir_turn = 0
    turn_go = 0
    while (x_begin > req_x_num) or (y_begin > req_y_num):
        #плавный старт
        if d_begin < math.pi:
            d_begin = d_begin + math.pi/10
            velocity = velocity + math.sin(d_begin)
        velocity = velocity * 2

        x_add = velocity * math.cos(fi_angle)  # находим координату X прирощения
        y_add = velocity * math.sin(fi_angle)  # находим координату Y прирощения

        x_begin += x_add  # находим конечную координату X
        y_begin += y_add  # находим конечную координату Y
        print(velocity, direction, turn_go, dir_turn, 'другое прямо')
        list_ = [velocity, direction, turn_go, dir_turn]
        list_size = link.tx_obj(list_)
        send_size = list_size
        link.send(send_size)
        time.sleep(0.4)

    return x_begin, y_begin

def turn_right(value):
    dir_turn = 1
    turn_go = 1
    while not link.available():
        pass
    rcved_turn = link.rx_obj(obj_type=list,
                             obj_byte_size=2, list_format='h')
    while rcved_turn[0] > value:
        while not link.available():
            pass
        rcved_turn = link.rx_obj(obj_type=list,
                                 obj_byte_size=2, list_format='h')
        print(velocity, direction, turn_go, dir_turn, rcved_turn[0], 'направо')
        list_ = [velocity, direction, turn_go, dir_turn]
        list_size = link.tx_obj(list_)
        send_size = list_size
        link.send(send_size)

    k = 0
    while k <= 3:
        k = k + 1
        turn_go = 0
        print(velocity, direction, turn_go, dir_turn)
        list_ = [velocity, direction, turn_go, dir_turn]
        time.sleep(1)

def turn_left(value):
    # налево
    dir_turn = 0
    turn_go = 1
    while not link.available():
        pass
    rcved_turn = link.rx_obj(obj_type=list,
                                 obj_byte_size=2, list_format='h')
    while rcved_turn[0] < value:
        while not link.available():
            pass
        rcved_turn = link.rx_obj(obj_type=list,
                                     obj_byte_size=2, list_format='h')
        print(velocity, direction, turn_go, dir_turn, rcved_turn[0], 'налево')
        list_ = [velocity, direction, turn_go, dir_turn]
        list_size = link.tx_obj(list_)
        send_size = list_size
        link.send(send_size)
    k = 0
    while k<=3:
        k = k + 1
        turn_go = 0
        print(velocity, direction, turn_go, dir_turn)
        list_ = [velocity, direction, turn_go, dir_turn]
        time.sleep(1)

def stop_machine():
    velocity = 0
    turn_go = 0
    dir_turn = 0
    direction = 1
    print(velocity, direction, turn_go, dir_turn)
    list_ = [velocity, direction, turn_go, dir_turn]
    list_size = link.tx_obj(list_)
    send_size = list_size
    link.send(send_size)


def turning_var_1():
    coord = test_func(370, 400, math.radians(90), 370, 320)

    #остановка
    stop_machine()

    # налево
    turn_left(610)

    angle = angle_direction(5.25, 0, coord[0], coord[1], 180, 0)

    stop_machine()

    # направо
    turn_right(550)

    test_func_2(angle[0], 320, math.radians(270), angle[0], angle[1])

    stop_machine()

def turning_var_2():
    coord_straight_1 = test_func(10370, 10360, math.radians(90), 10370, 10320)

    stop_machine()

    turn_left(610)

    coord_angle_1 = angle_direction(4.6, 90, coord_straight_1[0], coord_straight_1[1], 180)

    stop_machine()

    turn_right(550)

    coord_straight_2 = test_func_backward(coord_angle_1[0] + 320, coord_angle_1[1], math.radians(180),
                                                     coord_angle_1[0], coord_angle_1[1])

    stop_machine()

    turn_left(610)

    coord_angle_2 = angle_direction(4.6, coord_angle_1[2], coord_straight_2[0], coord_straight_2[1], 90)

    stop_machine()

    turn_right(550)

    coord_straight_3 = test_func_2(10370, 10320, math.radians(270),
                                                coord_angle_2[0], coord_angle_1[1])
    stop_machine()

turning_var_2()