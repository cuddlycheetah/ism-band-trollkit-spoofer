from modulators.OOKModulator import OOKModulator
import numpy as np
"""
Intertek Remote Sockets
"""
class Intertek_Clone_RemoteSocket:
    def __init__(self, baseband_samplerate=2e6):
        self.modulator = OOKModulator(baseband_samplerate=baseband_samplerate, am_frequency=22.471e3)
    def test(self):
        print("Intertek Clone Remote Sockets (433MHz)")
    def generateSamples(self, systemCode=7, deviceCode=1, state=True, numpyType=np.complex64):
        for i in range(6):
            # Systemcode
            SC1 = systemCode & 0x1
            SC2 = (systemCode >> 1) & 0x1
            SC3 = (systemCode >> 2) & 0x1
            SC4 = (systemCode >> 3) & 0x1
            SC5 = (systemCode >> 4) & 0x1

            SC1 = 1
            SC2 = 1
            SC3 = 1
            SC4 = 0
            SC5 = 0

            # Devicecode
            GC1 = 0# if deviceCode == 3 else 0
            GC2 = 0#0 if deviceCode == 0 else 1
            GC3 = 0# if deviceCode == 1 else 0
            GC4 = 1# if deviceCode == 3 else 1
            # Status
            STATE = int(state)
            bits = [ 
                1,SC1,1,SC2,1,SC3,1,SC4,1,SC5,
                1,GC1,1,GC2,1,GC3,1,GC4,
                1,0,1, STATE,1,1 - STATE,1 
            ]
            print(bits)
            for j in bits:
                if int(j) == 1:
                    self.modulator.addModulation(320)
                    self.modulator.addPadding(1060)
                else:
                    self.modulator.addModulation(1060)
                    self.modulator.addPadding(320)
            self.modulator.addPadding(10660 -1060) # Packet Sync

        return self.modulator.getSamplesAndReset(numpyType)