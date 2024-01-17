# setup the ball size
"""
R - for radius
p - for плотность
V = 4/3 * pi * r^3
L = distance between ball and bucket
H - height bucket from tha ground
S - size of the shield
BucketR - bucket radius
some parabola
matplotlib
"""

from math import radians, degrees

import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin

time_line = np.linspace(0, 30, 3500)

g = 9.81
# in metres
bucket_r = 0.23
ball_r = 0.11
H = 3.05
h = 1.05
L = 5
human_height = 1.7
height = H + h

angle_ranges = [radians(i) for i in range(10, 90, 5)]
velocity_ranges = [i for i in range(1, 50 + 1, 5)]
print("We will test:")
print("Angle ranges: ", angle_ranges)
print("Velocity ranges: ", velocity_ranges)
# format> [x0, x1], [y0, y1]
shield_line = np.matrix([[L, L], [H, H + h]])
bucket_line = np.matrix([[L - 2 * bucket_r, L], [H, H]])


def get_Y(v0, a, t):
    return (v0 * sin(a) * t) - ((g / 2) * t ** 2)


def get_X(v0, a, t):
    return v0 * cos(a) * t


# building system lines

def array_check_shield(X, Y):
    for i in range(len(X)):
        if check_shield_impact(X[i], Y[i]):
            return True
    return False


def get_time_impact_shield(X, Y):
    for i in range(0, len(time_line_cutted)):
        if check_shield_impact(X[i], Y[i]):
            return i


def array_circle_impact_clear(X, Y):
    # смотрим с сеередины, потому чтобы мяч попал чисто, нужно чтобы он начал уже падать
    for i in range(len(X) // 2, len(X)):
        if check_circle_impact(X[i], Y[i]):
            return True
    return False


def array_circle_impact_from_shield(X, Y):
    for x in X:
        for y in Y:
            if check_circle_impact(x, y):
                return True
    return False


def check_shield_impact(x, y):
    return (H <= y <= (height + 0.05)) and ((L - 0.1) <= x <= L)


def check_circle_impact(x, y):
    if (((L - 2 * bucket_r) <= x <= (L)) and ((H - 0.05) <= y <= (H + 0.05))):
        print(x, y)
        return True
    return False


# def trim_x:
#     pass
def trim_y(y):
    return [i for i in y if i < H + h]


plt.plot([L, L], [H, H + h])
plt.plot([L - 2 * bucket_r, L], [H, H])
# plt.plot([x0, x1], [y0, y1], 'b')
plt.plot([0, L], [0, 0], 'b')
# plt.text(point1[0]-0.015, point1[1]+0.25, "Point1")
# plt.text(point2[0]-0.050, point2[1]-0.25, "Point2")


for v0 in [12]:
    print("Now testiing v = ", v0, " m/s")
    for a in [radians(45)]:
        print("With angle a = ", degrees(a), " degrees")
        print("Calculating trajectory without impact")

        y = [get_Y(v0, a, t) for t in time_line if get_Y(v0, a, t) >= 0]
        x = [get_X(v0, a, t) for t in time_line][:len(y)]
        time_line_cutted = time_line[:len(y)]
        # states = np.array(
        #     [[x,y,t] for x in X for y in Y for t in time_line_cutted ]
        # )

        plt.plot(x, y, '--')

        print("Checking impact on shield or circle")
        if array_check_shield(x, y):
            print("Making inverse trajectory")
            idx = get_time_impact_shield(x, y)
            impact_time = time_line_cutted[idx]
            plt.plot(x[:idx], y[:idx], ':')

            v0_new = -v0
            print(idx)
            x_reversed = [get_X(v0_new, a, time_line_cutted[t]) for t in range(idx, len(time_line_cutted))]
            x_new = x[:idx] + x_reversed
            print("Checking circle impact")
            if array_circle_impact_from_shield(x_new, y):
                plt.plot(x_new[:len(y)], y, ':')
            print("no score even now")

        elif array_circle_impact_clear(x, y):

            print("Hitted score!")

            if len(y) > len(x):
                plt.plot(x, y[:len(x)], '--')
            else:
                plt.plot(x[:len(y)], y, '--')

        else:
            print("no score....")

        # new_x_matrix, new_y_matrix = trim_zone([get_X(v0, a, t) for t in time_line],
        #                                        [get_Y(v0, a, t) for t in time_line if get_Y(v0, a, t) >= 0])

        # if check_shield_impact(x,y) and not check_circle_impact(x,y):
        #     if len(new_y_matrix) > len(new_x_matrix):
        #         plt.plot(new_x_matrix, new_y_matrix[:len(new_x_matrix)], '--')
        #     else:
        #         plt.plot(new_x_matrix[:len(new_y_matrix)], new_y_matrix, '--')
        # checking if we are beating the shield -> trim x y
        # checking if we in circle -> trim x y
plt.ylabel('$y(t)$', fontsize=20)
plt.xlabel('$x(t)$', fontsize=20)
plt.show()

# if check_overfly(x_matrix,y_matrix):
# plt.plot(x_matrix[:len(trim_y(y_matrix))], trim_y(y_matrix), '--')
