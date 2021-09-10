
ComplexString="4f00f64f"
#get first two characters
N=2
length= len(ComplexString)
typeHex=ComplexString[:2]

def location (testString):
    polarityHex=testString[2:4]
    polarityInt=int(polarityHex, base=16)
    if (polarityInt==0):
        latitudePosition="S"
        longitudePosition="W"
    elif(polarityInt==1):
        latitudePosition="S"
        longitudePosition="E"
    elif(polarityInt==10):
        latitudePosition="N"
        longitudePosition="W"
    elif(polarityInt==11):
        latitudePosition="N"
        longitudePosition="E"
    else:
        print("Polarity not defined")
  

    # getting the latitude

    latitudeHex=testString[4:12]
    latitudeInt=int(latitudeHex,base=16)
    latitudeOriginal=float(latitudeInt/1000000)
    lat=str(latitudeOriginal)+" " +latitudePosition

    #getting the longitude
    longitudeHex=testString[12:20]
    longitudeInt=int(longitudeHex,base=16)
    longitudeOriginal=float(longitudeInt/1000000)
    long=str(longitudeOriginal)+" " +longitudePosition

    return lat, long

def battery (testString):

    batteryhex=testString[length - N: ]
    batteryInt=int(batteryhex, base=16)
    return batteryInt

def level (testString):
    levelhex=testString[2:6]
    levelInt=int(levelhex, base=16)
    return levelInt

if (typeHex=="1f"):
    #getting the polarity
    
    deviceLat, deviceLong=location(ComplexString)
    deviceBat=battery(ComplexString)

    print(deviceBat, deviceLat, deviceLong)

elif (typeHex=="2f"):
    waterLevel=level(ComplexString)
    deviceBat=battery(ComplexString)
    print(deviceBat, waterLevel)
elif (typeHex=="4f"):
    waterLevel=level(ComplexString)
    deviceBat=battery(ComplexString)
    print(deviceBat, waterLevel)
else:
    deviceBat=battery(ComplexString)
    print(deviceBat)
