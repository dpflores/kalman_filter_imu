
import os
import serial

DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\data"
DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "\data\data.txt"

def clear_file(filename):
  file = open(filename,"w")
  file.close()

def write_to_file(dt, wx, wy, wz, ax, ay, az):
    
    with open(DATA_FILE, 'a') as file:
        file.write(str(dt) + ", " + str(wx) + ", " + str(wy) + ", " + str(wz) + ", " + str(ax) + ", " + str(ay) + ", " + str(az) + "\n")
        file.close()


def main():

  if not os.path.exists(DATA_FOLDER):
    # Create a new directory because it does not exist 
    os.makedirs(DATA_FOLDER)
    print("The new directory is created!")


  # Init and clear files
  clear_file(DATA_FILE)
  print("File cleared")

  
    


  port = "COM3"

  ser = serial.Serial(port, 115200, timeout=1)

  print('Writing...')
  while True:
      data = ser.readline()
      data_sensor = data.decode()
      data_sensor = data_sensor.split(', ')
      if len(data_sensor)==7:
          dt = float(data_sensor[0])
          ax = float(data_sensor[1])
          ay = float(data_sensor[2])
          az = float(data_sensor[3])
          wx = float(data_sensor[4])
          wy = float(data_sensor[5])
          wz = float(data_sensor[6])
          
          write_to_file(dt, wx, wy, wz, ax, ay, az)

main()