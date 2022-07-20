import numpy as np
import matplotlib.pyplot as plt
import os

DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "/data/data.txt"

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

th_x_kal = [0]
th_y_kal = [0]

th_x_comp = [0]
th_y_comp = [0]


# Initial angular positions
xk = np.array([[0, 0]]).T

# Initial output
yk = np.array([[0, 0]]).T
# Initial angular speeds
uk = np.array([[0, 0]]).T

# Initial covariance
Pk = 0.01*np.eye(2)  

graph_data = open(DATA_FILE,'r').read()
lines = graph_data.split('\n')

for line in lines:
    if len(line) > 1:
        dt, wx, wy, wz, ax, ay, az = line.split(', ')

        # Updating stimates
        theta_x_w.append(theta_x_w[-1] + float(dt)*wx_a[-1]/131)
        theta_y_w.append(theta_y_w[-1] + float(dt)*wy_a[-1]/131)

        theta_x = np.arctan(float(ay)/np.sqrt(float(ax)**2 + float(az)**2))*(180.0/3.14)
        theta_x_a.append(theta_x)
        theta_y = np.arctan(-float(ax)/np.sqrt(float(ay)**2 + float(az)**2))*(180.0/3.14)
        theta_y_a.append(theta_y)

        th_x_comp.append( 0.98*(th_x_comp[-1] + (float(wx)/131)*float(dt)) + 0.02*theta_x)
        th_y_comp.append( 0.98*(th_y_comp[-1] + (float(wy)/131)*float(dt)) + 0.02*theta_y)
        

        # Getting new data
        t_a.append(t_a[-1] + float(dt))
        wx_a.append(float(wx))
        wy_a.append(float(wy))
        wz_a.append(float(wz))
        
        ax_a.append(float(ax))
        ay_a.append(float(ay))
        az_a.append(float(az))
        


        Fk = np.array([[1.0, 0.0],
                        [0.0, 1.0]])

        Gk = np.array([[float(dt)/131, 0.0],
                        [0.0, float(dt)/131]])

        Hk = np.array([[1.0, 0.0],
                        [0.0, 1.0]])

        Q = np.array([[(0.25**2)*float(dt)**2, 0.0],
                        [0.0, (0.86**2)*float(dt)**2]])

        R = np.array([0.06**2, 0.1**2]).T
        
        
        # 1 Prediction
        xk = Fk @ xk + Gk @ uk
        Pk = Fk @ Pk @ Fk.T + Q

        # 2a Optimal gain
        Kk = Pk @ Hk @ np.linalg.inv(Hk @ Pk @ Hk.T + R)

        # 2b correction
        xk = xk + Kk @ (yk - Hk @ xk)
        Pk = (np.eye(2) - Kk @ Hk) @ Pk

        th_x_kal.append(xk[0,0])
        th_y_kal.append(xk[1,0])

        # print(Kk)

        # Updating
        uk = np.array([[float(wx), float(wy)]]).T
        yk = np.array([[theta_x, theta_y]]).T
    

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ax1.plot(t_a, theta_x_w, 'b-')
ax1.plot(t_a, theta_x_a, 'r-')
ax1.plot(t_a, th_x_kal, 'g-')
ax1.plot(t_a, th_x_comp, 'y-')

ax2.plot(t_a, theta_y_w, 'b-')
ax2.plot(t_a, theta_y_a, 'r-')
ax2.plot(t_a, th_y_kal, 'g-')
ax2.plot(t_a, th_y_comp, 'y-')

# fig2 = plt.figure()
# plt.plot(t_a, Kk_a)

plt.show()