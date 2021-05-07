# PythonArduinoControl
A fast communication method between python and Arduino boards. Useful when testing controllers on a real system but you dont have professional gear  

-----------------
# Introduction
I have created this project as we all know testing something on a proper setup is complicated in times of Corona. However, suppose you have this simple Arduino board and some electrical components, it is likely you could build a simple system such as a Buck Converter at home! Therefore, you can actually test your controller on a real system.

Why not MATLAB?
I know MATLAB would be much easier as you likely already have your controller made in MATLAB. However both the Arduino library and the Serial stream library are incredibly slow. Even including delays to "improve" communication. My tests on an Arduino UNO showed that the arduino library achieved a sampling rate of 16Hz and the Serial Stream library a sampling rate of 25Hz (0.06 and 0.04 seconds for each Read / Write cycle). Needless to say, for an electrical system, this is an incredibly low rate. The implementation using python achieves sampling rates 10x higher.

What does this do?
The goal of this little piece of code is to achieve the fastest possible communication between the pc and the arduino board. This is achieved through the following means:
- Baudrate of 115200 (duh)
- Serial communication is in bytes, not chars. So example scripts show that you can send the value 112 in 3 bytes: ('1', '1', '2') each as a ASCII character. This code however sends it as one byte (112 or 'p'). As such, there is much less overhead in the data communication.
- Communication works in a fire-and-forget logic, so does not needs acknowledgements (this can be changed)
- PWM frequency in the Arduino board has been changed to 960Hz (default) to 62500Hz. This is to reduce the effect of the switching behaviour in the system.

So in total, there are 3 things you can do:
1. Request the voltage value of pin A0 (value between 0 and 1024). The PC will send 1 byte and the arduino returns 2.
2. Set a new PWM duty cycle on pin D6 (value between 0 and 255). The PC will send 2 bytes and immediately continues.
3. Same as 2 but with an acknowledgement. The PC will send 2 bytes and waits untill the arduino returns 1. This ensures the PWM value is updated before the python script continues (and thus removes the input delay).

From own implementations, if you dont use the acknowledgement in the input script, you can run it at roughly 250Hz (0.004s). With the acknowledgement the sampling rate decreases significantly, to roughly 125Hz (0.008s), so be aware.

-----------------
# Liability
I am not responsible for anything you do with this software and any damage caused by it.
This code has not been tested on computers operating with Linux or MACOS operating systems. I can only confirm that it works on my Win10 device.

-----------------
# Requirements
- Arduino IDE (download can be found at their website)
- Any Python IDE
- the PySerial package (pip install pyserial)
