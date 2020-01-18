#!/usr/bin/env python
import argparse
import math
import signal
import time

import numpy as np

import protocols.Nexus

nexus = protocols.Nexus.Nexus_TempHumidity()
data2 = nexus.generateData(244, 1, 0, 100)

from modulators.OOKModulator import OOKModulator

A = 1

ookTest = OOKModulator(baseband_samplerate=2e6, am_frequency=22.471e3)
for i in range(6):
    # 7x0 Preamble + Code
    #   1 = 10 10 00 10
    #   2 = 10 10 10 00
    #   3 = 10 00 10 10
    #   4 = 00 10 10 10
    #           Systemcode
    SC1 = 1
    SC2 = 1
    SC3 = 1
    SC4 = 0
    SC5 = 0

    GC1 = 1
    GC2 = 0
    GC3 = 1
    GC4 = 1

    STATE = 1
    bits = [ 1,SC1,1,SC2,1,SC3,1,SC4,1,SC5,1,GC1,1,GC2,1,GC3,1,GC4,1,0,1, STATE,1,1 - STATE,1  ]
    for j in bits:
        if int(j) == 0:
            ookTest.addModulation(1060)
            ookTest.addPadding(320)
        else:
            ookTest.addModulation(320)
            ookTest.addPadding(1060)
    ookTest.addPadding(10660 -1060) # Packet Sync

output = ookTest.getSamples(np.complex64)

with open('output.complex', 'wb') as f:
    output.tofile(f)