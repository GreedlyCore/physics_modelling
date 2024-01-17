from numpy import sin, cos, round
import numpy as np
from fractions import Fraction


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


# without air resistance
class trajectory:
    g = 9.81

    # initial states for all variables
    # angle in radians
    # k for coeffisient of air resistance
    def __init__(self, h, v, angle, k, step):
        self.angle = angle
        self.v = v
        self.n = 0
        self.x = 0
        self.y = h
        self.v_x = v * cos(angle)
        self.v_y = v * sin(angle)
        self.a_y = - self.g - k * v * sin(angle)
        self.a_x = -k * v * cos(angle)
        self.k = k
        self.step = step
        self.bucket_hit = False
        self.shield_hit = False
        self.prev_states = [
            {"order": 0, "x": self.x, "y": self.y, "v_x": self.v_x, "v_y": self.v_y, "a_x": self.a_x, "a_y": self.a_y,
             "time": 0}]

    # get next point of trajectory
    # step ~ time step

    def calculate(self):
        while True:
            next = self.next()
            if next is not None:
                if not self.shield_hit:
                    self.check_shield(self.prev(), self.now())
                self.check_bucket(self.prev(), self.now())
                if self.bucket_hit:
                    print("hitted bucket")
                    break
                if self.now()["x"] > L:
                    break
            else:
                break

    def get_final_coords(self):
        data = self.get_all_prev()
        return data[-1]["x"], data[-1]["y"]

    def get_plot_data(self):
        data = self.get_all_prev()
        x = [i["x"] for i in data]
        y = [i["y"] for i in data]
        return x, y

    def next(self):
        n, x_prev, y_prev, v_x_prev, v_y_prev, a_x_prev, a_y_prev, time_prev = self.prev_states[-1].values()

        x = round(x_prev + v_x_prev * self.step, 4)
        y = round(y_prev + v_y_prev * self.step, 4)
        v_x = round(v_x_prev + a_x_prev * self.step, 4)
        v_y = round(v_y_prev + a_y_prev * self.step, 4)
        a_x = round(- self.k * v_x_prev,4)
        a_y = round(- self.g - self.k * v_y_prev,4)
        time = round(time_prev + self.step,4)
        state = {"order": self.n, "x": x, "y": y, "v_x": v_x, "v_y": v_y, "a_x": a_x, "a_y": a_y, "time": time}
        if y >= 0:
            self.n += 1
            self.prev_states.append(state)
            return state
        else:
            return None

    # def next(self):
    #     n, x_prev, y_prev, v_x_prev, v_y_prev, a_x_prev, a_y_prev, time_prev = self.prev_states[-1].values()
    #
    #     x = x_prev + v_x_prev * self.step
    #     y = y_prev + v_y_prev * self.step
    #     v_x = v_x_prev + a_x_prev * self.step
    #     v_y = v_y_prev + a_y_prev * self.step
    #     a_x = - self.k * v_x_prev
    #     a_y = - self.g - self.k * v_y_prev
    #     time = time_prev + self.step
    #     state = {"order": self.n, "x": x, "y": y, "v_x": v_x, "v_y": v_y, "a_x": a_x, "a_y": a_y, "time": time}
    #     if y >= 0:
    #         self.n += 1
    #         self.prev_states.append(state)
    #         return state
    #     else:
    #         return None

    def add(self, x, y, v_x, v_y, a_x, a_y, time):
        state = {"order": self.n, "x": x, "y": y, "v_x": v_x, "v_y": v_y, "a_x": a_x, "a_y": a_y, "time": time}
        self.n += 1
        self.prev_states.append(state)

    def get_all_prev(self):
        return self.prev_states

    def is_bucket_hitted(self):
        return self.bucket_hit

    def is_shield_hitted(self):
        return self.shield_hit

    def now(self):
        return self.prev_states[-1]

    def prev(self):
        return self.prev_states[-2]



    # сравнить приближение эйлера для шагов эйлера 0.001 0.002 нарисовать траектории сравнить в 2.5
    #  показать, что ударяется
    # мы рисуем траекюторию центра масс
    # для трёх разумных углов
    # график модели сделать точками!!! крестиками
    # подтреждение того, что шаг - адекватный
    # интеравктивность посмотреть
    def check_bucket(self, state_prev, state_now):
        global left_bucket, right_bucket
        if state_prev["y"] >= H + ball_r >= state_now["y"] and \
                right_bucket - ball_r >= state_prev["x"] >= left_bucket + ball_r and \
                right_bucket - ball_r >= state_now["x"] >= left_bucket + ball_r:
            self.bucket_hit = True

    def check_shield(self, state_prev, state_now):
        global low_shield, high_shield
        if Fraction(state_now["x"]) > L- ball_r >= Fraction(state_prev["x"] ) and \
                high_shield > Fraction(state_prev["y"]) > low_shield and \
                high_shield > Fraction(state_now["y"]) > low_shield:
            n, x_prev, y_prev, v_x_prev, v_y_prev, a_x_prev, a_y_prev, time_prev = state_prev.values()
            step = abs(x_prev - L) / v_x_prev
            x = L - ball_r
            y = y_prev + v_y_prev * step
            v_x = - (v_x_prev + a_x_prev * step)
            v_y = v_y_prev + a_y_prev * step
            a_x = - self.k * v_x_prev
            a_y = - self.g - self.k * v_y_prev

            time = time_prev + step
            self.prev_states.pop()
            self.add(x, y, v_x, v_y, a_x, a_y, time)
            self.shield_hit = True
        #     print("checking shield->true")
        # print("checking shield->false")
        self.shield_hit=False


class perfect_trajectory:
    def __init__(self, h, v, angle):
        self.angle = angle
        self.step = 0.005
        self.v = v
        self.n = 0
        self.x = 0
        self.y = h
        self.v_x = v * cos(angle)
        self.v_y = v * sin(angle)
        self.bucket_hit = False
        self.shield_hit = False
        self.prev_states = [
            {"order": 0, "x": self.x, "y": self.y, "v_x": self.v_x, "v_y": self.v_y,"time": 0}]


    def calculate(self):
        while True:
            next = self.next()
            if next is not None:
                if not self.shield_hit:
                    self.check_shield(self.prev(), self.now())
                self.check_bucket(self.prev(), self.now())
                if self.bucket_hit:
                    print("hitted bucket")
                    break
                if self.now()["x"] > L:
                    break
            else:
                break

    def get_final_coords(self):
        data = self.get_all_prev()
        return data[-1]["x"], data[-1]["y"]

    def get_plot_data(self):
        data = self.get_all_prev()
        x = [i["x"] for i in data]
        y = [i["y"] for i in data]
        return x, y

    def next(self):
        n, x_prev, y_prev, v_x_prev, v_y_prev, time_prev = self.prev_states[-1].values()

        x = round(x_prev + v_x_prev * self.step, 4)
        y = round(y_prev + v_y_prev * self.step, 4)
        v_x = v_x_prev
        v_y = round(v_y_prev - g * self.step, 4)
        time = round(time_prev + self.step,4)
        state = {"order": self.n, "x": x, "y": y, "v_x": v_x, "v_y": v_y, "time": time}
        if y >= 0:
            self.n += 1
            self.prev_states.append(state)
            return state
        else:
            return None

    def add(self, x, y, v_x, v_y, a_x, a_y, time):
        state = {"order": self.n, "x": x, "y": y, "v_x": v_x, "v_y": v_y, "time": time}
        self.n += 1
        self.prev_states.append(state)

    def get_all_prev(self):
        return self.prev_states

    def is_bucket_hitted(self):
        return self.bucket_hit

    def is_shield_hitted(self):
        return self.shield_hit

    def now(self):
        return self.prev_states[-1]

    def prev(self):
        return self.prev_states[-2]



    # сравнить приближение эйлера для шагов эйлера 0.001 0.002 нарисовать траектории сравнить в 2.5
    #  показать, что ударяется
    # мы рисуем траекюторию центра масс
    # для трёх разумных углов
    # график модели сделать точками!!! крестиками
    # подтреждение того, что шаг - адекватный
    # интеравктивность посмотреть
    def check_bucket(self, state_prev, state_now):
        global left_bucket, right_bucket
        if state_prev["y"] >= H + ball_r >= state_now["y"] and \
                right_bucket - ball_r >= state_prev["x"] >= left_bucket + ball_r and \
                right_bucket - ball_r >= state_now["x"] >= left_bucket + ball_r:
            self.bucket_hit = True

    def check_shield(self, state_prev, state_now):
        global low_shield, high_shield
        if Fraction(state_now["x"]) > L >= Fraction(state_prev["x"] + ball_r) and \
                high_shield > Fraction(state_prev["y"]) > low_shield and \
                high_shield > Fraction(state_now["y"]) > low_shield:
            n, x_prev, y_prev, v_x_prev, v_y_prev, time_prev = state_prev.values()
            step = abs(x_prev - L) / v_x_prev
            x = L - ball_r
            y = y_prev + v_y_prev * step
            v_x = - v_x_prev
            v_y = v_y_prev - g * step

            time = time_prev + step
            self.prev_states.pop()
            self.add(x, y, v_x, v_y, time)
            self.shield_hit = True
        self.shield_hit=False