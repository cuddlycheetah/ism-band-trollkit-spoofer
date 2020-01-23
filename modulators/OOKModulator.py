import numpy as np

def generateAMSine(fs, toneFreq, numSamples, amplitude):
    step = (float(toneFreq) / float(fs)) * 2.0 * np.pi
    phaseArray = np.array(range(0,numSamples)) * step
    #e^(j*theta) = cos(theta) + j * sin(theta)
    wave = np.exp(1.0j * phaseArray) * amplitude

    return wave
class OOKModulator:
    def __init__(self, baseband_samplerate, am_frequency):
        self.baseband_samplerate = baseband_samplerate
        self.am_frequency = am_frequency
        self.samples = generateAMSine(self.baseband_samplerate, 0, 1000, 0)
    def addPadding(self, uSDuration):
        sampleCount = int((uSDuration / 1000000.0) * self.baseband_samplerate)
        self.samples = np.append(self.samples, generateAMSine(self.baseband_samplerate, 0, sampleCount, 0))
    def addModulation(self, uSDuration):
        sampleCount = int((uSDuration / 1000000.0) * self.baseband_samplerate)
        self.samples = np.append(self.samples, generateAMSine(self.baseband_samplerate, self.am_frequency, sampleCount, 1))
    def getSamples(self, numpyType):
        self.addPadding(1000)
        return self.samples.astype(numpyType)
    def getSamplesAndReset(self, numpyType):
        self.addPadding(1000)
        returnSamples = self.samples.astype(numpyType)
        self.samples = generateAMSine(self.baseband_samplerate, 0, 1000, 0)
        return returnSamples
