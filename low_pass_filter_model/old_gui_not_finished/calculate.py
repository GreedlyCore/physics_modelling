from numpy import sin, cos, round
import numpy as np
from mpl_toolkits.axisartist.axislines import SubplotZero
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp


def rungekutta4(f, t):
    x = [0]  # выходное напряжение
    j = 0
    h = 0.1  # разбиение
    while j < 100:
        i = int(j / h)  # целочисленный итератор
        k0 = h * f(t[i], x[i])
        k1 = h * f(t[i] + 0.5 * h, x[i] + 0.5 * k0)
        k2 = h * f(t[i] + 0.5 * h, x[i] + 0.5 * k1)
        k3 = h * f(t[i] + h, x[i] + k2)
        x.append(x[i] + (1 / 6) * (k0 + 2 * k1 + 2 * k2 + k3))
        j = round(j + h, 1)
    return x
    # n = len(t)
    # y = n*[0]
    # y[0] = 0
    # for i in range(n - 1):
    #     h = t[i+1] - t[i]
    #     k1 = f(y[i], t[i])
    #     k2 = f(y[i] + k1 * (h / 2), t[i] + (h / 2))
    #     k3 = f(y[i] + k2 * (h / 2), t[i] + (h / 2))
    #     k4 = f(y[i] + k3 * h, t[i] + h)
    #     y[i+1] = y[i] + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
    # return y

def euler_method(f,t):
    n = len(t)
    s = n*[0]
    h = t[1] - t[0]
    for i in range(0, len(t) - 1):
        s[i + 1] = s[i] + h*f(s[i],t[i])
    return s


class signal:
    def __init__(self, form, C, R, r, E0, f, t):
        self.U0 = E0
        self.f = f
        self.C = C
        self.t = t
        self.r = r
        self.R = R
        self.form = form
        self.Out = []
        self.In = []
        self.Final= []
        self.omega = 2 * 3.14159 * self.f
        self.sin_wave = self.U0 * np.sin(self.omega*self.t)

        
    
    def calculate_in(self):
        self.sin_wave = self.U0 * np.sin(self.omega*self.t)
        self.In = [self.t, self.get_wave()]
    
    def calculate_final(self):

        f_old = self.f
        f = [10, 20, 40, 60, 100, 200, 300, 600, 800, 10**3, 2*10**3, 4*10**3, 7*10**3, 10**4, 20*10**3,25*10**3,40*10**3,50*10**3,60*10**3,70*10**3,80*10**3,90*10**3, 10**5]
        
        sols = []
        for F in f:
            self.set_f(F)
            self.calculate_out()
            sols.append(max(self.get_Out_plot_data()[1]))
        
        self.set_f(f_old)
        print(sols)
        self.Final = [f,  sols]


    def dvdt(self, U, t):
            # print(f"VARS:{self.r} | {self.C} | {self.r} | {self.R}")
            return  (1/(self.r*self.C)) * (self.get_wave_func(t) - U*(1 + (self.r/self.R)) ) 


    def calculate_out(self):
        self.Out = [self.t, rungekutta4(self.dvdt, self.t)]
        

    def set_form(self, form):
        self.form = form

    def get_wave(self):
        if self.form == "sin wave":
            return self.sin_wave
        elif self.form == "half wave":
             return np.maximum(self.sin_wave, 0)
        elif self.form == "full wave":
            return np.abs(self.sin_wave)
    
    def get_wave_func(self, time):
        sin_wave = self.U0 * np.sin(self.omega * time)
        if self.form == "sin wave":
            return sin_wave
        elif self.form == "half wave":
             return np.maximum(sin_wave, 0)
        elif self.form == "full wave":
            return np.abs(sin_wave)
    
    def set_C(self, C):
        self.C = C

    def set_R(self, R):
        self.R = R

    def set_f(self, f):
        self.f = f
    def set_r(self, r):
        self.r = r
    def set_E0(self, E0):
        self.U0 = E0
    def set_t(self, t):
        self.t = t


    def get_In_plot_data(self):
        return self.In

    def get_Out_plot_data(self):
        return self.Out
    
    def get_Final_plot_data(self):
        return self.Final