import numpy as np
import matplotlib.pyplot as plt


# ALREADY SETTED UP IN FILE --> init.txt
# C = 2.12 * 10 ** -8  # емкость
# E0 = 10  # амплитуда ЭДС гениератора
# R = 10 ** 5  # Сопротивление нагрузки
# r = 3000 # сопротивление

# setup_vars()
with open('low_pass_filter_model\\ready\init.txt') as file:
    lines = [line.rstrip() for line in file]
C = eval(lines[0])
E0 = eval(lines[1])
R = eval(lines[2])
r = eval(lines[3])
    


f_cut_off = round(1 / (2 * np.pi * C * r))

# sin wave 
def E1(t, w):
    return E0 * np.sin(w*t)  
# ???? wave     
def E2(t, w):  
    if np.sin(w*t) < 0:
        return 0
    else:
        return E0 * np.sin(w*t)
# half wave 
def E3(t, w):
    return np.maximum(E1(t,w), 0)
# full wave 
def E4(t, w):
    return np.abs(E1(t,w))

def E5(t, w):
    return np.where(np.sin(w*t) > 0, E0, -E0)

def eq(E, t, v, w):  # диффур правая часть
    return (1/(r*C)) * (E(t, w) - v * (1 + r / R))


def runge_kutta4(E, w, t):
    x = [0]  
    h = (t[1] - t[0]) / 2
    for i in range(len(t) - 1):
        k0 = h * eq(E, t[i], x[i], w)
        k1 = h * eq(E, t[i] + 0.5 * h, x[i] + 0.5 * k0, w)
        k2 = h * eq(E, t[i] + 0.5 * h, x[i] + 0.5 * k1, w)
        k3 = h * eq(E, t[i] + h, x[i] + k2, w)
        x.append(x[i] + (1 / 6) * (k0 + 2 * k1 + 2 * k2 + k3))
    return x


# Зависимость напряжения от времени:
def time(E, f, t):
    plt.figure(f"experiment_{N}")
    w = f * 2 * np.pi

    # Динамическая t - создание
    T1 = (1/(f))
    delta_t = min ((1/10), (1/10)*T1)
    T = np.linspace(0,3*T1, 5*int((3-0)/delta_t) )

    x = runge_kutta4(E, w, T)

    plt.plot(T*10**5, [E(i, w)  for i in T],'b', label="E(t) - input voltage") 
    plt.plot(T*10**5, x, 'g', label="U(t) - output voltage") 
    plt.grid()
    plt.title(f'Частота среза: {f_cut_off} Гц \n Частота генератора: {round(f)} Гц')
    plt.legend(loc="upper left")
    plt.xlabel('$t$, мс')
    plt.ylabel('$V$, В')
    
# АЧХ:
def plot_f_cut_off(E, freqs, t):
    plt.figure(f"f_cut_off - plot")
    u_max = []  
    for f in freqs:
        w = 2 * np.pi * f

        # Динамическая t - создание
        T1 = (1/(f))
        delta_t = min ((1/10), (1/10)*T1)
        T = np.linspace(0,3*T1, 5*int((3-0)/delta_t) )

        u_max.append(max(runge_kutta4(E, w, T)))


    plt.plot([f_cut_off for _ in u_max], u_max, label="$f_{cut}$")  
    plt.plot(freqs, u_max)  
    plt.grid()
    plt.xlabel('f, Гц')
    plt.ylabel('V, none')
    plt.legend(loc="upper right")
    plt.title(f'Амплитудно-частотная характеристика\nЧастота среза: {f_cut_off} Гц')
    

freq_list = [f_cut_off*0.1,f_cut_off*0.2, f_cut_off, 5*f_cut_off]
t = np.linspace(0, 120*10**-5, 600)
N = 15
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
    time(E, freq, t)
    N+=1  

freq_list_big = d = f_cut_off*np.array([i/20 for i in range(1,60+1)] )

plot_f_cut_off(E, freq_list_big, t)  
plt.show()