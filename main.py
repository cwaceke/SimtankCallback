# rahog52419@rerunway.com,whereWasGondor

from flask import Flask, request, render_template
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
# 3 slashes is a relative path
#now to initialise our dB

db=SQLAlchemy(app)

class Data(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    device_id=db.Column(db.String(50))
    time=db.Column(db.String(50))
    data=db.Column(db.String(50),nullable=False)
    battery=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String(60))
    level=db.Column(db.Integer)

    
    def to_dict(self):
        return {
            'device_id':self.device_id , 
            'time':self.time, 
            'data':self.data, 
            'battery':self.battery, 
            'location':self.location, 
            'level':self.level
        }
db.create_all()

def getDate():
    now_date=datetime.now().astimezone()
    d= now_date.strftime("%m/%d/%y, %H:%M")
    return d


def locationPin (testString):
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

    N=2
    length= len(testString)

    batteryhex=testString[length - N: ]
    batteryInt=int(batteryhex, base=16)
    return batteryInt

def level (testString):
    levelhex=testString[2:6]
    levelInt=int(levelhex, base=16)
    return levelInt

@app.route('/')
def index():
    data=Data.query
    return(render_template('index.html', data=data))

@app.route('/uipage')
def uipage():
    data=Data.query
    return(render_template('uipage.html', data=data))


@app.route('/device/<device_id>')
def device(device_id):
    data=Data.query.filter_by(device_id=device_id).all()

    return render_template('device.html', data=data)   

@app.route('/confirmation', methods=['POST'])
def confirmation():
    
    content=request.json #grab the json data
    device_id=content['id']
    dataString=content['data']
    time = getDate()
    typeHex=dataString[:2]
    if (typeHex=="1f"):
    #getting the polarity
    
        deviceLat, deviceLong=locationPin(dataString)
        deviceBat=battery(dataString)
        deviceLoc=deviceLat+" "+deviceLong
        #previous=Data.select().order_by(Data.time.desc()).filter_by(Data.device_id==device_id)
        #print (previous)
        #previous_level=previous.device_id

        new_data=Data(device_id=device_id, time=time, data=dataString, battery=deviceBat,location=deviceLoc)

    elif (typeHex=="2f"):
        waterLevel=level(dataString)
        deviceBat=battery(dataString)
        new_data=Data(device_id=device_id, time=time,data=dataString, battery=deviceBat,level=waterLevel)
       
    elif (typeHex=="4f"):
        waterLevel=level(dataString)
        deviceBat=battery(dataString)
        new_data=Data(device_id=device_id, time=time,data=dataString, battery=deviceBat,level=waterLevel)
        
    else:
        deviceBat=battery(dataString)
        new_data=Data(device_id=device_id, time=time, data=dataString, battery=deviceBat)


    file=open('confirm.json','a')
    file.write(json.dumps(content))
    file.close()
    db.session.add(new_data)
    db.session.commit()
    print (new_data)
    return ('', 200)
    

    
