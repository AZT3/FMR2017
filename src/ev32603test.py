#!/usr/bin/env python3

import time, sys
from random import randint
from ev3dev.auto import *
import inspect
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *

# Configure motors
motors = [LargeMotor(address) for address in (OUTPUT_B, OUTPUT_C)]
assert all([m.connected for m in motors]), \
    "Two large motors should be connected to ports B and C"

# Configure infrared sensor
ultra_sensor = UltrasonicSensor()
assert ultra_sensor.connected

# Configure touch sensor
ts = TouchSensor()
assert ts.connected

# Configure Gyroscope Sensor
gyro_sensor = GyroSensor()
assert gyro_sensor.connected

# Configure Color Sensor
ty = ColorSensor()
assert ty.value


def start(dc):
    for m in motors:
        m.reset()
        m.run_forever(duty_cycle_sp=dc, polarity='normal')

def stop():
    for m in motors:
        print("stopping", m)
        m.stop()

def turn():
    power = (1, -1)
    t = randint(250, 1000)

    for m, p in zip(motors, power):
        m.run_timed(duty_cycle_sp=p*75, time_sp=t)

    while any(m.state for m in motors):
        time.sleep(0.1)

def backup():
    # Sound backup alarm.
    Sound.tone([(1000, 500, 500)] * 3)

    # Break and go back
    for m in motors:
        m.stop(stop_command='brake')
        m.run_timed(duty_cycle_sp=-50, time_sp=1500)

    while any(m.state for m in motors):
        time.sleep(0.1)

# Start all motors
dc = 50
start(dc)

r = open('gyrodata.txt', 'w+')
f = open('data.txt', 'w+')
p = open('colordata.txt', 'w+')
i = open('motor1data.txt', 'w+')
mi = open('motor2data.txt', 'w+')
sp = open('speed.txt', 'w+')
spi = open('speed1.txt', 'w+')

btn = Button()
while not btn.any(): 
    if ts.value():
        # Rear touch sensor pressed, maybe we're stuck, backup
        backup()
        turn()
        start(50)
        continue

    # Read proximity sensor
    d = ultra_sensor.value()
    print(d)

    e = gyro_sensor.value()
    print(e)
    
    y = ty.color()
    print(y)    

    mt = motors[0].count_per_rot
    mt1 = motors[1].count_per_rot
    print(mt)
    print(mt1)
    spr = motors[0].speed
    spr1 = motors[1].speed
    print(spr)
    print(spr1)

    r.write(str(e)+'\n')
    f.write(str(d)+'\n')
    p.write(str(y)+'\n')    
    i.write(str(mt)+'\n')
    mi.write(str(mt1)+'\n')
    sp.write(str(spr)+'\n')
    spi.write(str(spr1)+'\n')
    start(dc)

    if d > 300:
        # Full speed
        dc = 90
    elif d > 280:
        # Half speed, obstacle ahead
        dc = 45
    else:
        # Obstacle too close, turn
        stop()
        Sound.speak('Obstaku lo hevitado').wait()
        turn()
    
    time.sleep(0.1)

# Stop all motors
stop()
