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

# format> [x0, x1], [y0, y1]
shield_line = np.matrix([[L, L], [H, H + h]])
bucket_line = np.matrix([[L - 2 * bucket_r, L], [H, H]])

plt.plot([L, L], [H, H + h])
plt.plot([L - 2 * bucket_r, L], [H, H])
plt.plot([0, L], [0, 0], 'b')

angle_ranges = [radians(i / 10) for i in range(200, 800, 5)]
velocity_ranges = [i for i in range(10, 25 + 1, 3)]
print("Angle ranges: ", [degrees(i) for i in angle_ranges])
print("Velocity ranges: ", velocity_ranges)

# 0.05 -> 20 times/per second
# 0.01 -> 100 times/per second
for v in velocity_ranges:
    for a in angle_ranges:
        print("now: ", v, degrees(a))
        resolver = trajectory(human_height, v, a, 0.3, 0.01)
        resolver.calculate()
        if resolver.is_bucket_hitted():
            x, y = resolver.get_plot_data()
            plt.plot(x, y, '--')

plt.ylabel('$y, m$', fontsize=10)
plt.xlabel('$x, m$', fontsize=10)
plt.show()

