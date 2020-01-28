from modulators.OOKModulator import OOKModulator
import numpy as np
"""
Nemaxx WL10 Smokedetectors
"""
class Nemaxx_WL10_SmokeDetector:
    def __init__(self, baseband_samplerate=2e6):
        self.modulator = OOKModulator(baseband_samplerate=baseband_samplerate, am_frequency=22.471e3)
    def test(self):
        print("Nemaxx WL10 Smokedetector (433MHz)")
    def generateSamples(self, repeatNum=20, numpyType=np.complex64):
        for i in range(repeatNum):
            bits = [0,1,0,0,0,1,1,1,0,1,0,1,1,0,1,1,1,1,1,0,1,0,1,0]
            print(bits)
            self.modulator.addModulation(8120)
            self.modulator.addPadding(912)
            for j in bits:
                self.modulator.addModulation(795)
                self.modulator.addPadding(1400 if int(j) == 0 else 2750)
            self.modulator.addModulation(795)
            self.modulator.addPadding(1337) # Packet Sync
            self.modulator.addPadding(20000)

        return self.modulator.getSamplesAndReset(numpyType)