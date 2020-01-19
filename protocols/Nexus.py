from modulators.OOKModulator import OOKModulator
import numpy as np
"""
Nexus Temperature & Humidity Protocol
"""
class Nexus_TempHumidity:
    def __init__(self):
        pass
    def generateData(self, id=244, channel=1, temp=30, humidity=100):
        nibbles = self.generatePacket(id, channel, temp, humidity)
        data = []
        for i in range(9):
            mask = 0x08
            for j in range(4):
                if (nibbles[i] & mask):
                    data.append(1)
                else:
                    data.append(0)
                mask >>= 1
        return data
    def generateSamples(self, baseband_samplerate=2e6, id=244, channel=1, temp=30, humidity=100, numpyType=np.complex64):
        modulator = OOKModulator(baseband_samplerate=baseband_samplerate, am_frequency=22.471e3)
        bits = self.generateData(id, channel, temp, humidity)
        for j in bits:
            modulator.addModulation(500)
            modulator.addPadding(1000 * (1 + int(j)))
        modulator.addModulation(500)
        modulator.addPadding(4000)
        return modulator.getSamplesAndReset(numpyType)

    def generatePacket(self, id=244, channel=1, temp=30, humidity=100):
        packet = [
            (id >> 4) & 0x0f,
            id & 0x0f,
            7 + channel,
            (temp >> 8) & 0x0f,
            (temp >> 4) & 0x0f,
            temp & 0x0f,
            0x0f,
            (humidity >> 4) & 0x0f,
            humidity & 0x0f
        ]
        return packet
