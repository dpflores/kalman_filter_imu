import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "/data/data.txt"

fig = plt.figure()


ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

t_a = [0]

wx_a = [0]
wy_a = [0]
wz_a = [0]

ax_a = [0]
ay_a = [0]
az_a = [0]

theta_x_w = [0]
theta_y_w = [0]
theta_x_a = [0]
theta_y_a = [0]

graph_data = open(DATA_FILE,'r').read()
lines = graph_data.split('\n')

for line in lines:
    if len(line) > 1:
        dt, wx, wy, wz, ax, ay, az = line.split(', ')

        # Updating stimates
        theta_x_w.append(theta_x_w[-1] + float(dt)*wx_a[-1]/131)
        theta_y_w.append(theta_y_w[-1] + float(dt)*wy_a[-1]/131)

        theta_x_a.append(np.arctan(float(ay)/np.sqrt(float(ax)**2 + float(az)**2))*(180.0/3.14))
        theta_y_a.append(np.arctan(float(ax)/np.sqrt(float(ay)**2 + float(az)**2))*(180.0/3.14))

        # Getting new data
        t_a.append(t_a[-1] + float(dt))
        wx_a.append(float(wx))
        wy_a.append(float(wy))
        wz_a.append(float(wz))
        
        ax_a.append(float(ax))
        ay_a.append(float(ay))
        az_a.append(float(az))

# DATA TO MODEL THE NOISES
# Getting the mean values of our data 
mean_x_w = np.mean(theta_x_w)*np.ones_like(theta_x_w)
mean_y_w = np.mean(theta_y_w)*np.ones_like(theta_y_w)
mean_x_a = np.mean(theta_x_a)*np.ones_like(theta_x_a)
mean_y_a = np.mean(theta_y_a)*np.ones_like(theta_y_a)

var_x_w = np.var(theta_x_w)
var_y_w = np.var(theta_y_w)
var_x_a = np.var(theta_x_a)
var_y_a = np.var(theta_y_a)

print(var_x_w, var_y_w)
print(var_x_a, var_y_a)

ax1.plot(t_a, theta_x_w, 'b-')
ax1.plot(t_a, mean_x_w, 'g-')
ax1.set_ylabel("gyroscope (°))")

ax3.plot(t_a, theta_x_a, 'b-')
ax3.plot(t_a, mean_x_a, 'g-')
ax3.set_xlabel("theta_x (s)")
ax3.set_ylabel("accelerometer (°)")


ax2.plot(t_a, theta_y_w, 'r-')
ax2.plot(t_a, mean_y_w, 'g-')

ax4.plot(t_a, theta_y_a, 'r-')
ax4.plot(t_a, mean_y_a, 'g-')
ax4.set_xlabel("theta_y (s)")



fig2 = plt.figure()
        
ax1 = fig2.add_subplot(2,2,1)
ax2 = fig2.add_subplot(2,2,2)
ax3 = fig2.add_subplot(2,2,3)
ax4 = fig2.add_subplot(2,2,4)

mu = [np.mean(theta_x_w), np.mean(theta_y_w), np.mean(theta_x_a), np.mean(theta_y_a)]
sigma = np.sqrt([var_x_w, var_y_w, var_x_a, var_y_a])

x0 = np.linspace(mu[0] - 3*sigma[0], mu[0] + 3*sigma[0], 100)
x1 = np.linspace(mu[1] - 3*sigma[1], mu[1] + 3*sigma[1], 100)
x2 = np.linspace(mu[2] - 3*sigma[2], mu[2] + 3*sigma[2], 100)
x3 = np.linspace(mu[3] - 3*sigma[3], mu[3] + 3*sigma[3], 100)


ax1.set_ylim((0,1.6))
ax2.set_ylim((0,1.6))
ax3.set_ylim((0,1.6))
ax4.set_ylim((0,1.6))

ax1.plot(x0, stats.norm.pdf(x0, mu[0], sigma[0]), 'b-')
ax1.set_ylabel("gyroscope")
ax2.plot(x1, stats.norm.pdf(x1, mu[1], sigma[1]), 'r-')
ax3.plot(x2, stats.norm.pdf(x2, mu[2], sigma[2]), 'b-')
ax3.set_ylabel("accelerometer")
ax3.set_xlabel("noise_x")
ax4.plot(x3, stats.norm.pdf(x3, mu[3], sigma[3]), 'r-')
ax4.set_xlabel("noise_y")


plt.show()
