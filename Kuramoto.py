import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


K_syn = []
t_syn = []
K_asyn = []
t_asyn = []
K_full_asyn = []
t_full_asyn = []
center = 0
# Задаем функцию, которая описывает дифференциальное уравнение
def kur2(phi, t, K, w1, w2, w3, T):
    phi1, phi2, phi3 = phi
    e = (np.exp(-t*1000/T))
    d = K*e
    dphi1 = w1 + (K/3) * (np.sin(phi2 - phi1) + np.sin(phi3 - phi1)) * e
    dphi2 = w2 + (K/3) * (np.sin(phi1 - phi2) + np.sin(phi3 - phi2)) * e
    dphi3 = w3 + (K/3) * (np.sin(phi1 - phi3) + np.sin(phi2 - phi3)) * e
    center = (dphi1+dphi2+dphi3)/3
    if (abs(dphi1-center) <= 0.0005 and abs(dphi2-center)<=0.0005 and abs(dphi3-center)<=0.0005):
        K_syn.append(d)
        t_syn.append(t)
    if (dphi1 == w1 and dphi2 == w2 and dphi3 == w3):
        K_full_asyn.append(d)
        t_full_asyn.append(t)

    return [dphi1, dphi2, dphi3]

# Задаем начальные условия
tfin = 480
K = 100
phi0 = np.random.rand(3) * 2 * np.pi
w1 = (1/35)
w2 = (1/50)
w3 = (1/25)  



# Интегрируем дифференциальное уравнение с помощью метода ode45
t = np.arange(0, tfin, 0.001)
sol = odeint(kur2, phi0, t, args=(K, w1, w2, w3, tfin))



if (len(K_syn) != 0):
    K_syn_start = K_syn[0]
    t_syn_start = t_syn[0]
    print(f'K_syn = {K_syn_start :.3f}, t_syn = {t_syn_start :.3f}')

if (len(t_syn)!=0):
    K_asyn_start = K_syn[-1]
    t_asyn_start = t_syn[-1]
    print(f'Lenght of Synhronization = {t_asyn_start - t_syn_start :.3f}')
    print(f'K_asyn = {K_asyn_start :.3f}, t_asyn = {t_asyn_start :.3f}')

K_full_asyn_start = K_full_asyn[0]
t_full_asyn_start = t_full_asyn[0]

print(f'K_full_asyn = {K_full_asyn_start :.3f}, t_full_asyn = {t_full_asyn_start :.3f}')



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
if (len(K_syn) != 0):
    plt.plot(t_syn_start, center, 'ro', label='K_syn')
    plt.plot(t_asyn_start, center, 'bo', label='K_asyn')
plt.plot(t_full_asyn_start, center, 'go', label='K_full_asyn')
plt.legend()
plt.show()
