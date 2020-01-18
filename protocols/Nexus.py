
class Nexus_TempHumidity:
    def __init__(self):
        self.test()
    def test(self):
        print("Nexus Temperature & Humidity Sensor")
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
