import time
import numpy as np
import SoapySDR
from SoapySDR import * #SOAPY_SDR_* constants

# Protocol part
import protocols.Nemaxx_WL10_SmokeDetector

nemaxx = protocols.Nemaxx_WL10_SmokeDetector.Nemaxx_WL10_SmokeDetector()
with open('output.complex', 'wb') as f:
    samples = nemaxx.generateSamples(repeatNum=10, alarmTheSlave=True)
    samples.tofile(f)

"""

## Transmit Part
SDR_ARGS = {'driver': 'lime'}

sdr = SoapySDR.Device(SDR_ARGS)

sdr.setSampleRate(SOAPY_SDR_TX, 0, 2e6)
sdr.setAntenna(SOAPY_SDR_TX, 0, 'Auto')
sdr.setFrequency(SOAPY_SDR_TX, 0, 433.92e6)
#sdr.setGain(SOAPY_SDR_TX, 0, 10)
print(sdr.listAntennas(SOAPY_SDR_TX, 0))
print("Actual Tx Rate %f Msps"%(sdr.getSampleRate(SOAPY_SDR_TX, 0) / 1e6))

txStream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32 , [0])
sdr.activateStream(txStream)

t0 = sdr.getHardwareTime()
tLate = t0 + int(1e8)
stream_mtu = sdr.getStreamMTU(txStream)
buff0 = np.ones(1024, np.complex64)
print(buff0)
buff1 = np.zeros(stream_mtu, np.complex64)
flags = SOAPY_SDR_HAS_TIME | SOAPY_SDR_END_BURST
time.sleep(1.0) #make sure the writeStream is late
sdr.writeStream(txStream,
    [buff0, buff1], 1024,
    flags=flags,
    timeNs=tLate,
    timeoutUs=int(1e6))

time.sleep(0.1)

sdr.deactivateStream(txStream)
sdr.closeStream(txStream)
"""