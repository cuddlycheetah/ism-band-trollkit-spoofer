#!/usr/bin/env python
import argparse
import math
import signal
import time

import numpy as np

import protocols.Nexus

nexus = protocols.Nexus.Nexus_TempHumidity()
data2 = nexus.generateData(244, 1, 0, 100)
print(data2)
print(len(data2))
from modulators.OOKModulator import OOKModulator

A = 1
import struct
def binary(num):
    # Struct can provide us with the float packed into bytes. The '!' ensures that
    # it's in network byte order (big-endian) and the 'f' says that it should be
    # packed as a float. Alternatively, for double-precision, you could use 'd'.
    packed = struct.pack('!f', num)
    print 'Packed: %s' % repr(packed)

    # For each character in the returned string, we'll turn it into its corresponding
    # integer code point
    # 
    # [62, 163, 215, 10] = [ord(c) for c in '>\xa3\xd7\n']
    integers = [ord(c) for c in packed]
    print 'Integers: %s' % integers

    # For each integer, we'll convert it to its binary representation.
    binaries = [bin(i) for i in integers]
    print 'Binaries: %s' % binaries

    # Now strip off the '0b' from each of these
    stripped_binaries = [s.replace('0b', '') for s in binaries]
    print 'Stripped: %s' % stripped_binaries

    # Pad each byte's binary representation's with 0's to make sure it has all 8 bits:
    #
    # ['00111110', '10100011', '11010111', '00001010']
    padded = [s.rjust(8, '0') for s in stripped_binaries]
    print 'Padded: %s' % padded

    # At this point, we have each of the bytes for the network byte ordered float
    # in an array as binary strings. Now we just concatenate them to get the total
    # representation of the float:
    return ''.join(padded)
print(binary(25.1))


ookTest = OOKModulator(baseband_samplerate=2e6, am_frequency=22.471e3)
for i in range(4):
    #bits = [ 0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,1,0,1,1,1 ]

    bitsStart = [ #statische 22Bit
        0,1,0,0,
        1,0,0,0,
        1,1,0,0,
        0,0,1,1,
        0,0,0,1,
        0,0,
    ]

    bits_23_7 = [
        0,0,
        1,1,1,1,
        1,1,0,1,
        0,1,1,1
    ]
    bits_23_4 = [
        0,0,
        1,1,1,1,
        1,0,1,0,
        0,1,0,0
    ]
    bits_25_1 = [
        0,0,
        1,1,1,1,
        1,0,1,1,
        0,1,1,0
    ]
    bits_31_6 = [
        0,1,
        0,0,1,1,
        1,1,0,0,
        1,1,0,0
    ]
    bits_34_1 = [
        0,1,
        0,1,0,1,
        0,1,0,1,
        0,1,1,1,
    ]
    bits_43_4 = [
        0,1,
        1,0,1,1,
        0,0,1,0,
        1,0,1,0
    ]
    bits_13_8 = [
        0,0,
        1,0,0,0,
        1,0,1,0,
        1,1,1,0
    ]
    bits_11_3 = [
        0,0,
        0,1,1,1,
        0,0,0,1,
        0,1,0,0
    ]
    bits_8_8 = [
        0,0,
        0,1,0,1,
        1,0,0,0,
        1,0,0,1
    ]
    bits = bitsStart + bits_43_4
    #bits = data2
    print(bits)
    print(len(bits))
    for j in bits:
        ookTest.addModulation(510)
        ookTest.addPadding(1010 * (1 + int(j)))
    ookTest.addModulation(510)
    ookTest.addPadding(4040) # Sync

output = ookTest.getSamples(np.complex64)

with open('output.complex', 'wb') as f:
    output.tofile(f)