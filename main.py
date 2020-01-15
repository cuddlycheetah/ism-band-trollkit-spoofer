import protocols.Nexus

nexus = protocols.Nexus.Nexus_TempHumidity()
print(nexus.generate(244, 1, 55, 100))
