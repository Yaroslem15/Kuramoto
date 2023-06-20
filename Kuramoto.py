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
d = 0
# Задаем функцию, которая описывает дифференциальное уравнение
def kur2(phi, t, K, w1, w2, w3, T):
    phi1, phi2, phi3 = phi
    e = (np.exp(-t*1000/T))
    d = K*e
    dphi1 = (w1 + (K/3) * (np.sin(phi2 - phi1) + np.sin(phi3 - phi1)) * e)
    dphi2 = (w2 + (K/3) * (np.sin(phi1 - phi2) + np.sin(phi3 - phi2)) * e)
    dphi3 = (w3 + (K/3) * (np.sin(phi1 - phi3) + np.sin(phi2 - phi3)) * e)
    center = (w1+w2+w3)/3
    if (abs(dphi1-center) <= 0.0005/k and abs(dphi2-center)<=0.0005/k and abs(dphi3-center)<=0.0005/k):
        K_syn.append(d)
        t_syn.append(t)
    if (dphi1 == w1 and dphi2 == w2 and dphi3 == w3):
        K_full_asyn.append(d)
        t_full_asyn.append(t)

    return [dphi1, dphi2, dphi3]

k = 1

# Задаем начальные условия
tfin = 480
K = 1000
phi0 = np.random.rand(3) * 2 * np.pi
w1 = (1/35)/k
w2 = (1/50)/k
w3 = (1/25)/k



# Интегрируем дифференциальное уравнение с помощью метода ode45
t = np.arange(0, tfin, 0.001)
sol = odeint(kur2, phi0, t ,args=(K, w1, w2, w3, tfin))



if (len(K_syn) != 0):
    K_syn_start = K_syn[0]
    t_syn_start = t_syn[0]
    print(f'K_syn = {K_syn_start :.3f}, t_syn = {t_syn_start :.3f}')

if (len(t_syn)!=0):
    K_asyn_start = K_syn[-1]
    t_asyn_start = t_syn[-1]
    print(f'Lenght of Synhronization = {t_asyn_start - t_syn_start :.3f}')
    print(f'K_asyn = {K_asyn_start :.3f}, t_asyn = {t_asyn_start :.3f}')

if (len(t_full_asyn) != 0):
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
plt.xlabel('t, мин')
plt.ylabel('w')

#k = max(wil[0],wi2[0],wi3[0])
#dw1 = np.arange(0, k, k//1)
#dw2 = np.diff(dw1)
#dw = dw2[0]

#if (len(K_syn) != 0):
#    plt.text(tfin/16, (center - 8*dw), f'K_syn = {K_syn_start :.3f}, t_syn = {t_syn_start :.3f}')
#    plt.text(tfin/16, (center - 6*dw), f'Lenght of synhronization = {t_asyn_start - t_syn_start :.3f}')
#    plt.text(tfin/16, (center - 4*dw), f'K_asyn = {K_asyn_start :.3f}, t_asyn = {t_asyn_start :.3f}')
#plt.text(tfin/16, (center - 2*dw), f'K_full_asyn = {K_full_asyn_start :.3f}, t_full_asyn = {t_full_asyn_start :.3f}')
if (len(K_syn) != 0):
    plt.plot(t_syn_start, center, 'ro', label='K_syn')
    plt.plot(t_asyn_start, center, 'bo', label='K_asyn')
if (len(t_full_asyn) != 0):
    plt.plot(t_full_asyn_start, center, 'go', label='K_full_asyn')

plt.legend()
plt.show()
