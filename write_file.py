
import os

DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "/data/data.txt"

def write_to_file(dt, wx, wy, wz, ax, ay, az):

  with open(DATA_FILE, 'a') as file:
    file.write(str(dt) + ", " + str(wx) + ", " + str(wy) + ", " + str(wz) + ", " + str(ax) + ", " + str(ay) + ", " + str(az) + "\n")
    file.close()