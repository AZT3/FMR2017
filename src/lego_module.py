__author__ = "Sergio Noriega Heredia"
__date__ = "$Mar 24, 2017 11:59:07 AM$"

from ev3dev.auto import *
from math import pi

def lego_init():
    motors=[LargeMotor(address) for address in (OUTPUT_A, OUTPUT_B, OUTPUT_C)]
    assert all([m.connected for m in motors])
    
    ultra_sensor=UltrasonicSensor()
    assert ultra_sensor.connected
    
    color_sensor=ColorSensor()
    assert color_sensor.connected
    
    gyro_sensor=GyroSensor()
    assert gyro_sensor.connected
    gyro_sensor.mode='GYRO-CAL'
    gyro_sensor.mode='GYRO-ANG'
    
    return {
    "motors":motors,
    "ultra_sensor":ultra_sensor,
    "color_sensor":color_sensor,
    "gyro_sensor":gyro_sensor
    }

def color_input(sensor):
    return sensor.color
    
def ultra_input(sensor):
    return sensor.distance_centimeters

def gyro_input(sensor):
    return sensor.angle

def motor_command(motors, velocity_polar, actual_angle):
    multiplier=50
    if(actual_angle>=pi): actual_angle-=2*pi
    dutyb=velocity_polar[0]*multiplier-(actual_angle-velocity_polar[1])*20
    if(dutyb>=100): dutyb=100
    elif(dutyb<-100): dutyb=-100
    dutyc=velocity_polar[0]*multiplier+(actual_angle-velocity_polar[1])*20
    if(dutyc>=100): dutyc=100
    elif(dutyc<-100): dutyc=-100
    motors[1].run_direct(duty_cycle_sp=dutyb)#B-left
    motors[2].run_direct(duty_cycle_sp=dutyc)#C-right
    return