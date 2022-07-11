// Librerias I2C para controlar el mpu6050
// la libreria MPU6050.h necesita I2Cdev.h, I2Cdev.h necesita Wire.h
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

// La dirección del MPU6050 puede ser 0x68 o 0x69, dependiendo 
// del estado de AD0. Si no se especifica, 0x68 estará implicito
MPU6050 sensor;

// Valores RAW (sin procesar) del acelerometro y giroscopio en los ejes x,y,z
int ax, ay, az;
int gx, gy, gz;

long tiempo_prev;
float dt;
float ang_x, ang_y;
float ang_x_prev, ang_y_prev;

void setup() {
  Serial.begin(115200);     //Iniciando puerto serial
  Wire.begin();             //Iniciando I2C  
  sensor.initialize();      //Iniciando el sensor

  if (sensor.testConnection()) Serial.println("Sensor iniciado correctamente");
  else Serial.println("Error al iniciar el sensor");
}

void loop() {
  // Leer las aceleraciones y velocidades angulares
  sensor.getAcceleration(&ax, &ay, &az);
  sensor.getRotation(&gx, &gy, &gz);
  
  dt = (millis()-tiempo_prev)/1000.0;
  tiempo_prev=millis();
  
  Serial.print(dt); 
  Serial.print(", ");
  Serial.print(ax); 
  Serial.print(", ");
  Serial.print(ay); 
  Serial.print(", ");
  Serial.print(az); 
  Serial.print(", ");
  Serial.print(gx); 
  Serial.print(", ");
  Serial.print(gy); 
  Serial.print(", ");
  Serial.println(gz); 

  delay(10);
}
