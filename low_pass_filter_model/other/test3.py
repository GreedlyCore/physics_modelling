import numpy as np
import matplotlib.pyplot as plt

def sinusoidal_step_wave(t, amp, duration):
    wave = np.where(np.sin(2 * np.pi * t / duration) > 0, amp, -amp)
    return wave

# Создание временной оси
t = np.linspace(0, 1, 1000)

# Задание амплитуды и продолжительности шага
amp = 2
duration = 0.5

# Создание синусоидальной step-волны с использованием определенных параметров
wave = sinusoidal_step_wave(t, amp, duration)

# Построение графика
plt.plot(t, wave)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Sinusoidal Step Wave')
plt.show()
