
class Nexus_TempHumidity:
    def __init__(self):
        self.test()
    def test(self):
        print("Nexus Temperature & Humidity Sensor")
    def generate(self, id=244, channel=1, temp=30, humidity=100):
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
