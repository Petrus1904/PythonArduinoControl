# -*- coding: utf-8 -*-
"""
Created on Thu May  6 12:44:11 2021

@author: Peter Verheijen
"""
import numpy as np
import matplotlib.pylab as plt
import serial
import time

## write data to the serial stream
def WriteInput(arduino, val, ReqAck = False):
    ## WriteInput
    #  @param arduino the serial communication object
    #  @param val the value the arduino should put on the PWM gate
    #  @param ReqAck, optional default = False. If true, it will send a new value
    #         and request an acknowledgement. once this Ack is received, the code continues
    assert isinstance(arduino, serial.Serial)
    assert isinstance(ReqAck, bool)
    val = int(min(max(0, val), 255))
    
    if(ReqAck == True):
        #Write 3 to arduino such that it expects a new input with Acknowledgement
        send = bytearray([3, val])
        arduino.write(send)
        # This acknowledgement means that after the Arduino applied the PWM signal
        # it will write 1 on the output. The line below makes this script wait untill
        # this value is received. Therefore it ensures the input is applied before
        # continuing to the next sample.
        # However, this delays the system to nearly half the sampling frequency.
        arduino.read(1)
    else:
        #Write 1 to arduino such that it expects a new input
        send = bytearray([1, val])
        arduino.write(send)

    return True

## Read the next line from the Serial stream
def GetOutput(arduino):
    ## GetOutput
    #  @param arduino the serial communication object
    #  @returns (int) the measured value from the analog in plug. value is always between 0 and 1024
    assert isinstance(arduino, serial.Serial)
    #this is required to prevent reading stuff that has been written before the request
    arduino.reset_input_buffer();
    #write 2 to arduino such that it returns the new output
    arduino.write((2).to_bytes(1, byteorder='big'))
    #output should be a value between 0 and 1023, thus it should be written in 2 bytes
    data = arduino.read(2)
    #first entry is the high byte, so every value larger than 255
    #second entry is everything below 255
    if(len(data) == 2):
        val = data[0]*256 + data[1]
        return val
    else:
        print(data)
        return 0
    
def ArduinoTest(arduino):
    assert isinstance(arduino, serial.Serial)
    x = np.linspace(0, 2*np.pi, 400)
    r = np.zeros_like(x)
    y = np.zeros_like(x)
    t = np.zeros_like(x)
    for i in range(0, 400):
        startTime = time.perf_counter()
        r[i] = 127*np.sin(x[i])+127
        WriteInput(arduino, int(r[i]))
        y[i] = GetOutput(arduino)
        t[i] = time.perf_counter() - startTime
        
    plt.plot(x, 4*r)
    plt.plot(x, y)
    plt.show()
    print('average sampling time: ', np.mean(t))
    
if __name__ == "__main__":
    # main routine
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1)
    # this is to let the arduino stuff initiate
    time.sleep(3)
    ArduinoTest(arduino)
    arduino.close()
    
    
    
    
    
    
    
    
    
    
    