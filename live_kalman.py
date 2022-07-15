from cv2 import KalmanFilter
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
        wx = float(raw_data[1])
        wy = float(raw_data[2])
        wz = float(raw_data[3])
        ax = float(raw_data[4])
        ay = float(raw_data[5])
        az = float(raw_data[6])

        # Correction sensor data
        theta_x = np.arctan(float(ay)/np.sqrt(float(ax)**2 + float(az)**2))*(180.0/3.14)
        theta_y = np.arctan(-float(ax)/np.sqrt(float(ay)**2 + float(az)**2))*(180.0/3.14)

        # Kalman matrices
        Fk = np.array([[1.0, 0.0],
                [0.0, 1.0]])
        Gk = np.array([[float(dt)/131, 0.0],
                        [0.0, float(dt)/131]])
        Hk = np.array([[1.0, 0.0],
                        [0.0, 1.0]])
        Q = np.array([[(0.25**2)*float(dt)**2, 0.0],
                        [0.0, (0.56**2)*float(dt)**2]])
        R = np.array([0.06**2, 0.1**2]).T


        # Prediction Step
        imu_kalman.prediction_step(Fk, Gk, Q)

        # Correction Step
        imu_kalman.correction_step(Fk, Gk, Q)
        
        # Updating
        imu_kalman.uk = np.array([[float(wx), float(wy)]]).T
        imu_kalman.yk = np.array([[theta_x, theta_y]]).T
    
       

        # x_angle = 45
        # y_angle = 45
        print(x_angle)
        delta_x = x_angle - current_x
        delta_y = y_angle - current_y
        delta_z = 0 # We dont have that angle since we are using MPU6050

        # We convert the IMU axis to the pygame axis using rotation matrix
        glRotatef(delta_x, 1, 0, 0)
        glRotatef(delta_z, 0, 1, 0)
        glRotatef(-delta_y, 0, 0, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        current_x = x_angle
        current_y = y_angle
        print(x_angle, ' ', y_angle)

        imu_prism.show_prism()
    