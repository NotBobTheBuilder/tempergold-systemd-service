#!/usr/bin/env python3
import os
import select
import struct

DEV = '/dev/hidraw1'

def read_temperature(device_path=DEV):
    # Credit to https://github.com/urwen/temper for this byte sequence
    QUERY = struct.pack('8B', 0x01, 0x80, 0x33, 0x01, 0x00, 0x00, 0x00, 0x00)
    
    # Open the device and return a file descriptor (needed for poll later)
    f = os.open(device_path, os.O_RDWR)
    
    # Write the "fetch temperature" query to the device
    os.write(f, QUERY)
    
    # Wait for the device to have data to read by polling the file descriptor
    poll = select.poll()
    poll.register(f, select.POLLIN)
    
    # This call blocks until data is ready
    poll.poll()
    poll.unregister(f)
    
    # Tempergold sends 16 bytes of data, read it and close the file
    data = os.read(f, 16)
    os.close(f)
    
    # Temperature is encoded as a big-endian 2 byte integer (aka short)
    # The encoded value represents degrees in c * 100
    return struct.unpack_from('>h', data, 2)[0] / 100

if __name__ == "__main__":
    print(read_temperature())
