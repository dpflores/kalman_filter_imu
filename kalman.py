import numpy as np


class KalmanFilter:
    def __init__(self, xk0, yk0, uk0, Pk0):
        # Initial angular positions
        self.xk = xk0   #np.array([[0, 0]]).T

        # Initial output
        self.yk = yk0   #np.array([[0, 0]]).T
        # Initial angular speeds
        self.uk = uk0   #np.array([[0, 0]]).T

        # Initial covariance
        self.Pk = Pk0   #0.01*np.eye(2)  
    
    def prediction_step(self, Fk, Gk, Q):
        # 1 Prediction
        self.xk = Fk @ self.xk + Gk @ self.uk
        self.Pk = Fk @ self.Pk @ Fk.T + Q
    
    def correction_step(self, Hk, R):
        # 2a Optimal gain
        Kk = self.Pk @ Hk @ np.linalg.inv(Hk @ self.Pk @ Hk.T + R)

        # 2b correction
        self.xk = self.xk + Kk @ (self.yk - Hk @ self.xk)
        self.Pk = (np.eye(np.shape(self.Pk)[0]) - Kk @ Hk) @ self.Pk