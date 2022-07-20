import numpy as np

from prism import *
from kalman import *

# Initialize prism
imu_prism = RectangularPrism()

# Setup display
imu_prism.setup_display()

# Serial setup
import serial
port = "COM3"
ser = serial.Serial(port, 115200, timeout=1)

# Kaman initialization
imu_kalman = KalmanFilter()
# Variable initialization
delta_x = 0
delta_y = 0
current_x = 0
current_y = 0

while True:
    data = ser.readline()
    data_sensor = data.decode()
    raw_data = data_sensor.split(', ')
    if len(raw_data)==7:
        dt = float(raw_data[0])
        ax = float(raw_data[1])
        ay = float(raw_data[2])
        az = float(raw_data[3])
        wx = float(raw_data[4])
        wy = float(raw_data[5])
        wz = float(raw_data[6])

        # Correction sensor data
        theta_x = np.arctan(ay/np.sqrt(ax**2 + az**2))*(180.0/3.14)
        theta_y = np.arctan(-ax/np.sqrt(ay**2 + az**2))*(180.0/3.14)

        # Kalman matrices
        Fk = np.array([[1.0, 0.0],
                [0.0, 1.0]])
        Gk = np.array([[dt/131, 0.0],
                        [0.0, dt/131]])
        Hk = np.array([[1.0, 0.0],
                        [0.0, 1.0]])
        Q = np.array([[(0.86**2)*dt**2, 0.0],
                        [0.0, (0.25**2)*dt**2]])
        R = np.array([0.06**2, 0.1**2]).T


        # Prediction Step
        imu_kalman.prediction_step(Fk, Gk, Q)

        # Correction Step
        imu_kalman.correction_step(Hk, R)

        # Resultant values
        x_angle = imu_kalman.xk[0,0]
        y_angle = imu_kalman.xk[1,0]

        # Updating
        imu_kalman.uk = np.array([[wx, wy]]).T
        imu_kalman.yk = np.array([[theta_x, theta_y]]).T
    
        
  
        delta_x = x_angle - current_x
        delta_y = y_angle - current_y
        delta_z = 0 # We dont have that angle since we are using MPU6050

        # We convert the IMU axis to the pygame axis using rotation matrix
        glRotatef(delta_x, 1, 0, 0)
        glRotatef(delta_z, 0, 1, 0)
        glRotatef(-delta_y, 0, 0, 1)

       
        current_x = x_angle
        current_y = y_angle
        print(x_angle, ' ', y_angle)

        imu_prism.show_prism()
    