from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID, BTLEException, Service, Characteristic
import string
import ctypes
import binascii

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

#   def handleDiscovery(self, dev, isNewDev, isNewData):
#        if isNewDev:
#            print ("Discovered device", dev.addr)
#        elif isNewData:
#            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(3)

#password: 000000
#my keyboard:"88:c6:26:ba:42:85"
#10 = indoor positioning service
#24:71:89:09:90:84

def angleToSignedInt(angleType):
    angleType = bytes(angleType, 'utf-8')
    angleType = binascii.a2b_hex(angleType)
    angleType = int.from_bytes(angleType, byteorder='big', signed=True)
    return angleType

for dev in devices:
    #print(dev.getScanData())
    #print(dev.addr)
    if dev.addr == "24:71:89:09:90:84":
        p = Peripheral("24:71:89:09:90:84")
        services = p.getServiceByUUID("F000AA80-0451-4000-B000-000000000000")
        characs = services.getCharacteristics()
        print(characs)
        actCharacs = bytes.fromhex("007F")
        print(actCharacs)
        angleMult = 360/255
        characs[1].write(actCharacs)
        while True:
            print(characs[0].read())
##            a = characs[0]read().hex()
##            a = str(a)
##            print(a)
##            X = a[0] + a[1]
##            Y = a[2] + a[3]
##            Z = a[4] + a[5]
##            angles = [X, Y, Z]
##            i = 0
##            for angleType in angles:
##                angles[i] = angleToSignedInt(angleType)
##                angles[i] *= angleMult
##                i += 1
##            print(angles)
        #servicesDict = p.getServices()
        #print(servicesDict)
        #print(servicesDict[1].getCharacteristics())
        #x = p.getCharacteristics()
        #print(x[12].getHandle())
        #print(p.readCharacteristic(x[12].getHandle()))
    
        #print(x[9].read())
        #print(x[9].getHandle())
##        servicesDict = str(servicesDict)
##        servicesList = servicesDict.split(",")
##        i = 0
##        for x in servicesList:
##            servicesList[i] = servicesList[i].strip(" <bluepy.btle.Service object at ")
##            servicesList[i] = servicesList[i].strip(">")
##            servicesList[i] = servicesList[i].strip(">])")
##            servicesList[i] = servicesList[i].strip("['dict_values([<bluepy.btle.Service object at ")
##            i += 1
##        print(servicesList)

##    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
##    for (adtype, desc, value) in dev.getScanData():
##        print ("  %s = %s" % (desc, value))
