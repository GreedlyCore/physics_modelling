import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import solve_ivp


t = np.linspace(0, 10, 800)


f = 150

omega = 2 * np.pi * f
# E0 - input voltage in V
E0 = 5


# Ёмкость конденсатора, Фарады
C = 10*-6
# Реактанта конденсатора
X_C  = 1/(omega*C)
# Резистор в фильтре, Ом
r = 10**3
# Внешняя нагрузка, Ом
R = 0.5*10**3

#  input_signal
def E(E0, omega, t):
    return E0 * np.cos(omega*t)

def dvdt(t, U):
    return (1/(r*C) * (E(E0, omega, t) - (1 + (r/R)* U )))
U0 = 0

sol_m1 = odeint(dvdt, y0=U0, t=t, tfirst=True)
v_sol_m1 = sol_m1.T[0]

plt.plot(t, v_sol_m1, 'b')
plt.plot(t, E(E0, omega, t),  'g')
plt.ylabel('$u(t)$', fontsize=22)
plt.xlabel('$t$', fontsize=22)
plt.show()