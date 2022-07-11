import os
import matplotlib.pyplot as plt
import numpy as np


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

# Getting the mean values of our data 
mean_x_w = np.mean(theta_x_w)*np.ones_like(theta_x_w)
mean_y_w = np.mean(theta_y_w)*np.ones_like(theta_y_w)
mean_x_a = np.mean(theta_x_a)*np.ones_like(theta_x_a)
mean_y_a = np.mean(theta_y_a)*np.ones_like(theta_y_a)

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
plt.show()

        

