import serial

port = "COM3"

ser = serial.Serial(port, 115200, timeout=1)

while True:
    data = ser.readline()
    data_sensor = data.decode()
    data_sensor = data_sensor.split(', ')
    if len(data_sensor)==7:
        print(data_sensor[6])

    