import numpy as np
import matplotlib.pyplot as plt

D = 1.05

times = [
    18.02,
    15.08,
    12.66,
    10.23,
    9.2,
    8.18,
    7.4,
    6.78,
    6.15,
    6.03,
    5.36,
    5.2,
    4.83,
    4.71,
    4.22
]
speed_tested = np.linspace(30, 100, 15)

speeds = []
for t in times:
    speeds.append(D/t)


plt.figure()
plt.title('Transosition de vitesse PWM en m/s')
plt.xlabel('Vitesse logique (PWM)')
plt.ylabel('Vitesse physique (m/s)')
plt.plot(speed_tested, speeds)
plt.show()


phi = []
row = []

ord = 2
order = range(0, ord)







