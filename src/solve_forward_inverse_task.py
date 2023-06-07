import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from math import radians, degrees

import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin

from src.Calculation import perfect_trajectory, trajectory


# def polynomial3(x, a, b, c, d):
#     return a * x ** 3 + b * x ** 2 + c * x + d
#
# def solve(x,y):
#     args, _ = curve_fit(polynomial3, x, y)
#     return args

# def polynomial4(x, a, b, c, d, e):
#     return a * x ** 4 + b * x ** 3 + c * x ** 2 + d*x + e
#
# def solve(x,y):
#     args, _ = curve_fit(polynomial4, x, y)
#     return args

# def polynomial5(x, a, b, c, d, e, f):
#     return a * x ** 5 + b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x + f

def polynomial2(x, a, b, c):
    return a * x ** 2 + b * x + c


def solve(x, y):
    args, _ = curve_fit(polynomial2, x, y)
    return args


# all units in SI system
g = 9.81
bucket_r = 0.23
ball_r = 0.11
H = 3.05
h = 1.05
L = 6.25
human_height = 1.7
height = H + h

left_bucket = L - 2 * bucket_r
right_bucket = L

low_shield = H
high_shield = H + h

# 0.05 -> 20 times/per second
# 0.01 -> 100 times/per second

def solve_velocity_inverse_task(X, Y):
    plt.plot([right_bucket - ball_r, right_bucket - ball_r], [v0, v1], '--')
    plt.plot([left_bucket + ball_r, left_bucket + ball_r], [v0, v1], '--')

    plt.ylabel('$v, м/c$', fontsize=10)
    plt.xlabel('$x, м$', fontsize=10)

    args = solve(Y, X, )
    X_approx = [polynomial2(y, *args) for y in Y]

    y1 = polynomial2(right_bucket - ball_r, *args)
    y2 = polynomial2(left_bucket + ball_r, *args)

    plt.text(max(Y) - 0.1, y1 + 0.1, '${} м/c$'.format(round(y1, 2)), fontsize=9)
    plt.text(max(Y) - 0.1, y2 + 0.1, '${} м/c$'.format(round(y2, 2)), fontsize=9)
    plt.plot([max(Y), min(Y)], [y1, y1], '--')
    plt.plot([max(Y), min(Y)], [y2, y2], '--')
    plt.plot(Y, X_approx, '--')
    plt.legend(['правая граница кольца', 'левая граница кольца', 'нижний предел углов', 'верхний предел углов',
                'аппроксимация'])
    plt.title('Решение обратной задачи для скоростей при $\\alpha$ = ' + str(round(degrees(a))), fontsize=12)
    plt.grid(True)
    plt.show()


def solve_velocity_forward_task(X, Y):
    plt.plot([v0, v1], [right_bucket - ball_r, right_bucket - ball_r], '--')
    plt.plot([v0, v1], [left_bucket + ball_r, left_bucket + ball_r], '--')

    plt.xlabel('$v, м/c$', fontsize=10)
    plt.ylabel('$x, м$', fontsize=10)

    # plt.plot(X, Y, marker='x')
    plt.plot(X, Y, 'x')

    args = solve(X, Y)
    Y_approx = [polynomial2(x, *args) for x in X]
    plt.plot(X, Y_approx)
    plt.legend(['правая граница кольца', 'левая граница кольца', 'моделирование', 'аппроксимация'])
    plt.title('Решение прямой задачи для скоростей при $\\alpha$ = ' + str(round(degrees(a))), fontsize=12)
    plt.grid(True)
    plt.show()


def solve_angles_forward_task(X, Y):
    # plt.plot([angle0, angle1], [right_bucket - ball_r, right_bucket - ball_r], '--')
    # plt.plot([angle0,angle1], [left_bucket + ball_r, left_bucket + ball_r], '--')

    plt.xlabel('$angle, \degree$', fontsize=10)
    plt.ylabel('$x, м$', fontsize=10)

    # plt.plot(X, Y, marker='x')
    plt.plot(X, Y, 'x')

    args = solve(X, Y)
    Y_approx = [polynomial2(x, *args) for x in X]
    plt.plot(X, Y_approx)
    plt.legend(['правая граница кольца', 'левая граница кольца', 'моделирование', 'аппроксимация'])
    plt.title('Решение прямой задачи для углов при v = ' + str(v), fontsize=12)
    plt.grid(True)
    plt.show()


def solve_angles_inverse_task(X, Y):
    plt.plot([right_bucket - ball_r, right_bucket - ball_r], [X[0], X[-1]], '--')
    plt.plot([left_bucket + ball_r, left_bucket + ball_r], [X[0], X[-1]], '--')

    plt.ylabel('$angle, \degree$', fontsize=10)
    plt.xlabel('$x, м$', fontsize=10)

    args = solve(Y, X, )
    X_approx = [polynomial2(y, *args) for y in Y]

    y1 = polynomial2(right_bucket - ball_r, *args)
    y2 = polynomial2(left_bucket + ball_r, *args)

    plt.text(max(Y) - 0.1, y1 + 0.1, '${}\degree$'.format(round(y1, 2)), fontsize=9)
    plt.text(max(Y) - 0.1, y2 + 0.1, '${}\degree$'.format(round(y2, 2)), fontsize=9)
    plt.plot([max(Y), min(Y)], [y1, y1], '--')
    plt.plot([max(Y), min(Y)], [y2, y2], '--')
    plt.plot(Y, X_approx, '--')
    plt.legend(['правая граница кольца', 'левая граница кольца', 'нижний предел углов', 'верхний предел углов',
                'аппроксимация'])
    plt.title('Решение обратной задачи для углов при v = ' + str(v), fontsize=12)
    plt.grid(True)
    plt.show()

# angle_ranges = [radians(i / 10) for i in range(200, 900, 1)]
# for v in [10, 16, 20]:
#     X1 = []
#     Y1 = []
#     for a in angle_ranges:
#         resolver = trajectory(human_height, v, a, 0.2, 0.05)
#         resolver.calculate()
#         x = resolver.get_final_coords()[0]
#         y = resolver.get_final_coords()[1]
#         if left_bucket + ball_r - 1 <= x <= right_bucket - ball_r + 1:
#             X1.append(degrees(resolver.angle))
#             Y1.append(x)
#     if len(X1) > 10 and len(Y1) > 10:
#         angle0 = degrees(angle_ranges[0])
#         angle1 = degrees(angle_ranges[-1])
#         solve_angles_forward_task(X1, Y1)
#         solve_angles_inverse_task(X1, Y1)
#     else:
#         print("not enough data1")

v_ranges = [i/10 for i in range(50,200+1, 1)]
for a in [radians(i) for i in [15,30,50]]:
    X2 = []
    Y2 = []
    for v in v_ranges:
        resolver = trajectory(human_height, v, a, 0.2, 0.05)
        resolver.calculate()
        x = resolver.get_final_coords()[0]
        y = resolver.get_final_coords()[1]
        if left_bucket + ball_r - 1 <= x <= right_bucket - ball_r + 1:
            X2.append(v)
            Y2.append(x)
    if len(X2) > 10 and len(Y2) > 10:
        v0 = v_ranges[0]
        v1 = v_ranges[-1]
        solve_velocity_forward_task(X2, Y2)
        solve_velocity_inverse_task(X2, Y2)
    else:
        print("not enough data2")
