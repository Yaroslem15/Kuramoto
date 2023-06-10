import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Задаем функцию, которая описывает дифференциальное уравнение
def kur2(phi, t, K, w1, w2, w3, T):
    phi1, phi2, phi3 = phi
    dphi1 = w1 + (K/3) * (np.sin(phi2 - phi1) + np.sin(phi3 - phi1)) * np.exp(-t/T)
    dphi2 = w2 + (K/3) * (np.sin(phi1 - phi2) + np.sin(phi3 - phi2)) * np.exp(-t/T)
    dphi3 = w3 + (K/3) * (np.sin(phi1 - phi3) + np.sin(phi2 - phi3)) * np.exp(-t/T)
    return [dphi1, dphi2, dphi3]

# Задаем начальные условия
tfin = 100
K = float(input("Введите коэффициент связи: "))                               # 0.385 (для 0.5, 0.75, 0.33)/ 0.375  (для 0.583, 0.833, 0.416)
phi0 = np.random.rand(3) * 2 * np.pi
w1 = float(input("Введите частоту первого осциллятора: "))
w2 = float(input("Введите частоту второго осциллятора: "))
w3 = float(input("Введите частоту третьего осциллятора: "))
T = tfin

# Интегрируем дифференциальное уравнение с помощью метода ode45
t = np.linspace(0, tfin, 1000)
sol = odeint(kur2, phi0, t, args=(K, w1, w2, w3, T))

# Вычисляем значения частот
wil = np.diff(sol[:, 0]) / np.diff(t)
wi2 = np.diff(sol[:, 1]) / np.diff(t)
wi3 = np.diff(sol[:, 2]) / np.diff(t)

# Визуализируем результаты
plt.plot(t[:-1], wil, label='wi1')
plt.plot(t[:-1], wi2, label='wi2')
plt.plot(t[:-1], wi3, label='wi3')
plt.xlabel('t')
plt.ylabel('frequency')
plt.legend()
plt.show()
