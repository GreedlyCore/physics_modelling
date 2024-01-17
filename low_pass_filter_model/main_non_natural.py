import numpy as np
import matplotlib.pyplot as plt


# ALREADY SETTED UP IN FILE --> init.txt
# C = 2.12 * 10 ** -8  # емкость
# E0 = 10  # амплитуда ЭДС гениератора
# R = 10 ** 5  # Сопротивление нагрузки
# r = 3000 # сопротивление

# setup_vars()
# C = 0; E0 = 0; R=0; r=0
with open('low_pass_filter_model\\ready\init.txt') as file:
    lines = [line.rstrip() for line in file]
C = eval(lines[0])
E0 = eval(lines[1])
R = eval(lines[2])
r = eval(lines[3])
    


f_cut_off = round(1 / (2 * np.pi * C * r))

# sin wave 
def E1(tau, W):
    return E0 * np.sin(W*tau)  
# ???? wave     
def E2(tau, W):  
    if np.sin(W*tau) < 0:
        return 0
    else:
        return E0 * np.sin(W*tau)
# half wave 
def E3(tau, W):
    return np.maximum(E1(tau,W), 0)
# full wave 
def E4(tau, W):
    return np.abs(E1(tau,W))

# sinusoidal step wave
def E5(tau, W):
    # amp = 2
    return np.where(np.sin(W*tau) > 0, E0, -E0)

def eq(E, tau, v, W):  # диффур правая часть
    return E(tau, W) / E0 - v * (1 + r / R)


def runge_kutta4(E, W, tau):
    x = [0]  
    h = (tau[1] - tau[0]) / 2
    for i in range(len(tau) - 1):
        k0 = h * eq(E, tau[i], x[i], W)
        k1 = h * eq(E, tau[i] + 0.5 * h, x[i] + 0.5 * k0, W)
        k2 = h * eq(E, tau[i] + 0.5 * h, x[i] + 0.5 * k1, W)
        k3 = h * eq(E, tau[i] + h, x[i] + k2, W)
        x.append(x[i] + (1 / 6) * (k0 + 2 * k1 + 2 * k2 + k3))
    return x


# Зависимость напряжения от времени:
def time(E, f, tau):


    plt.figure(f"experiment_{N}")
    W = f * 2 * np.pi * r * C  # циклическая частота генератора

    # Динамическая тау - создание
    T1 = (1/(f*r*C))
    delta_tau = min ((1/10), (1/10)*T1)
    TAU = np.linspace(0,3*T1, 5*int((3-0)/delta_tau) )

    x = runge_kutta4(E, W, TAU)
    

    
    print(f"lens: TAU: {len(TAU)} and x:{len(x)}")

    plt.plot(TAU, [E(i, W) / E0 for i in TAU],'b', label="E(t) - input voltage")  # /начальный сигнал генератора
    plt.plot(TAU, x, 'g', label="U(t) - output voltage") 
    plt.grid()
    plt.title(f'Частота среза: {f_cut_off} Гц \n Частота генератора: {round(f)} Гц')
    plt.legend(loc="upper left")
    plt.xlabel('$\\tau$')
    plt.ylabel('v')
    


# АЧХ:
def plot_f_cut_off(E, freqs, tau):
    plt.figure(f"f_cut_off - plot")
    u_max = []  # массив асплитудных значений напряжения на выходе

    

    for f in freqs:
        W = 2 * np.pi * f * r * C
        
        # Динамическая тау - создание
        T1 = (1/(f*r*C))
        delta_tau = min ((1/10), (1/10)*T1)
        TAU = np.linspace(0,3*T1, 5*int((3-0)/delta_tau) )

        u_max.append(max(runge_kutta4(E, W, TAU)))


    plt.plot([f_cut_off for _ in u_max], u_max, label="$f_{cut}$")  # прямая частоты среза
    plt.plot(freqs, u_max)  # АЧХ
    plt.grid()
    plt.xlabel('f, Гц')
    plt.ylabel('V, none')
    plt.legend(loc="upper right")
    plt.title(f'Амплитудно-частотная характеристика\nЧастота среза: {f_cut_off} Гц')
    

freq_list = [f_cut_off*0.1,f_cut_off*0.2, f_cut_off, 5*f_cut_off]


tau = np.linspace(0, 100, 600)

N = 9

# CHOOSE WAVE
if lines[4] == "E5":
    E = E5
elif lines[4] == "E4":
    E = E4
elif lines[4] == "E3":
    E = E3
elif lines[4] == "E2":
    E = E2
elif lines[4] == "E1":
    E = E1
    

for freq in freq_list:
    time(E, freq, tau)
    N+=1  # задаем входную частоту, массив времени, разбиение и строим v(t)

# freq_list_big = d = f_cut_off*np.array([i/10 for i in range(1,100+1)] )
# freq_list_big = d = f_cut_off*np.array([i/10 for i in range(1,20+1)] )
freq_list_big = d = f_cut_off*np.array([i/20 for i in range(1,60+1)] )

plot_f_cut_off(E, freq_list_big, tau)  # v(w), задачется начальное, конечное значение частоты и шаг
plt.show()