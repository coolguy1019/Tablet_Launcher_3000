import struct

import serial.tools.list_ports as port
import time
import serial
from serial.serialutil import SerialException


class COMMUNICATION:
    def __init__(self,baudrate,resettime,comport,timeout):

        try:
            self.ser = serial.Serial(comport, baudrate, timeout=timeout)
            time.sleep(resettime)
            self.ser.reset_input_buffer()  # resetting the input and output buffers
            self.ser.reset_output_buffer()
        except SerialException:
            print("close the serial monitor")
            self.ser = None





    def serialOutput(self,x_coord, y_coord, openess,sleeptime = 0.1):
        if self.ser is not None:
            binarydata = struct.pack('<BhhB',255,x_coord,y_coord,openess)
            self.ser.write(binarydata) #output format is "254,x,y,openess,255"
            time.sleep(sleeptime)



    def serialInput(self):
        if self.ser is  not None:
            if self.ser.in_waiting:  # readin the byte only when available.
                return self.ser.readline().decode()

    def close(self):
        if self.ser is not None:
            self.ser.close()


def get_ports():
    ports = port.comports()
    return ports





