
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
    device_id=db.Column(db.String(60))
    time=db.Column(db.DateTime, default=datetime.utcnow)
    data=db.Column(db.String(50),nullable=False)
    
    def __repr__ (self):
        return "(%s, %s, %s)" % (self.device_id , self.time, self.data)


ROWS_PER_PAGE=20
@app.route('/', methods=['GET', 'POST'], defaults={"page_num": 1})
@app.route('/<int:page_num>',methods=['GET', 'POST'])
def index(page_num):
    
    data=Data.query.order_by(Data.device_id.asc()).paginate(page=page_num, per_page=ROWS_PER_PAGE, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       data=Data.query.filter(Data.device_id.like(search)).paginate(page=page_num, per_page=ROWS_PER_PAGE,error_out=True)
       return render_template('index.html', data=data, tag=tag)
    return render_template('index.html', data=data)




@app.route('/confirmation', methods=['POST'])
def confirmation():
    
    content=request.json #grab the json data
    time_rough=int(content['time'])
    device_id=content['id']
    data=content['data']
    time = datetime.fromtimestamp(time_rough).strftime('%Y-%m-%d %H:%M:%S')
    print(time)
    print(device_id)
    print(data)
    file=open('confirm.json','a')
    file.write(json.dumps(content))
    file.close()
    new_data=Data(device_id=device_id, data=data)

    db.session.add(new_data)
    db.session.commit()
    return ('', 200)
    

    
