import matplotlib.pyplot as plt
import os

DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "/data/data.txt"

fig = plt.figure()


ax1 = fig.add_subplot(3,2,1)
ax2 = fig.add_subplot(3,2,2)
ax3 = fig.add_subplot(3,2,3)
ax4 = fig.add_subplot(3,2,4)
ax5 = fig.add_subplot(3,2,5)
ax6 = fig.add_subplot(3,2,6)


graph_data = open(DATA_FILE,'r').read()
lines = graph_data.split('\n')

t_a = [0]

wx_a = [0]
wy_a = [0]
wz_a = [0]

ax_a = [0]
ay_a = [0]
az_a = [0]

for line in lines:
    if len(line) > 1:
        dt, wx, wy, wz, ax, ay, az = line.split(', ')
        t_a.append(t_a[-1] + float(dt))
        wx_a.append(float(wx))
        wy_a.append(float(wy))
        wz_a.append(float(wz))
        
        ax_a.append(float(ax))
        ay_a.append(float(ay))
        az_a.append(float(az))


ax1.plot(t_a, wx_a, 'b-')
ax3.plot(t_a, wy_a, 'b-')
ax5.plot(t_a, wz_a, 'b-')
ax5.set_xlabel("angular speed")

ax2.plot(t_a, ax_a, 'r-')
ax4.plot(t_a, ay_a, 'r-')
ax6.plot(t_a, az_a, 'r-')
ax6.set_xlabel("acceleration")

plt.show()