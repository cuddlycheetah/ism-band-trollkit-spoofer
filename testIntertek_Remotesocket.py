from protocols.Intertek_RemoteSocket import Intertek_RemoteSocket
intertek = Intertek_RemoteSocket(2e6)
output = intertek.generateSamples(7, 3, True)

with open('output.complex', 'wb') as f:
    output.tofile(f)