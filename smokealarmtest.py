#!/usr/bin/env python
import argparse
import math
import signal
import time
import time
import SoapySDR
from SoapySDR import * #SOAPY_SDR_* constants


import numpy as np

import protocols.Nexus


from modulators.OOKModulator import OOKModulator

A = 1
import struct
def bitfield(n):
    return [int(digit) for digit in bin(n)[2:].zfill(8)]

ookTest = OOKModulator(baseband_samplerate=2e6, am_frequency=22.471e3)


for i in range(4):
    #bits = [ 0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,1,0,1,1,1 ]
    #bits = bitsUnitID[::-1]
    byte1 = 0x00
    byte2 = 0x00
    byte3 = 0x00

    PARAM_unit = 5 # max 30
    PARAM_id = 1337 # max 32767

    byte1 = PARAM_unit & 0x1f # | PARAM_id << 3
    byte2 = ((PARAM_id & 0x0f) >> 11)
    byte3 = 0x3
    



    print(bitfield(byte1))
    print(bitfield(byte2))
    print(bitfield(byte3))
    bits = bitfield(byte1)[::-1] + bitfield(byte2)[::-1] + bitfield(byte3)
    #bits = data2
    print(bits)
    print(len(bits))

    for bit in bits:
        if bit == 0:
            # Short Pulse
            ookTest.addModulation(436)
            ookTest.addPadding(1299)
        else:
            # Long Pulse
            ookTest.addModulation(1202)
            ookTest.addPadding(526)
        #Stop Pulse
        ookTest.addModulation(434)
        ookTest.addPadding(434)
        ookTest.addModulation(434)
        ookTest.addPadding(434)

output = ookTest.getSamples(np.complex64)

with open('output.complex', 'wb') as f:
    output.tofile(f)
"""
## Transmit Part
SDR_ARGS = {'driver': 'lime'}

sdr = SoapySDR.Device(SDR_ARGS)

sdr.setSampleRate(SOAPY_SDR_TX, 0, 2e6)
sdr.setAntenna(SOAPY_SDR_TX, 0, 'Auto')
sdr.setFrequency(SOAPY_SDR_TX, 0, 433.92e6)
sdr.setGain(SOAPY_SDR_TX, 0, 70)

txStream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32 , [0])
sdr.activateStream(txStream)
sdr.setHardwareTime(0)

flags = SOAPY_SDR_HAS_TIME | SOAPY_SDR_END_BURST
status = sdr.writeStream(txStream, [output], output.size, timeoutUs=1000000)

sdr.writeStream(txStream,
    output, output.size,
    #flags=flags,
    timeoutUs=int(1e6))


sdr.deactivateStream(txStream)
sdr.closeStream(txStream)
"""