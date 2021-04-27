from flask import Flask,request,render_template,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data.db'
db = SQLAlchemy(app)

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id = db.Column(db.Integer,primary_key=True)
    plate = db.Column(db.String(9),unique=True,nullable=False)
    driver = db.Column(db.String(100))
    color = db.Column(db.String(20))
    car_type = db.Column(db.String(50))
    is_ban = db.Column(db.Integer())
    comment = db.Column(db.String(200),nullable=True)
    #road_worthiness = db.Column(db.BLOB)
    #certificate = db.Column(db.BLOB)
    def __repr__(self):
        return f"{self.color} {self.car_type} - plate number:{self.plate}"

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/plates',methods=['GET'])
def get_vehicles():
        vehicles = Vehicle.query.all()
        output = []
        for vehicle in vehicles:
            vehicle_data = {'plate':vehicle.plate,'driver':vehicle.driver,'color':vehicle.color,'car_type':vehicle.car_type,'is_ban':vehicle.is_ban,'comment':vehicle.comment}
            output.append(vehicle_data)
        return {'vehicles':output}
    
@app.route('/plates/add',methods=['POST'])
def add_plate():
    vehicle = Vehicle(plate = request.json['plate'],driver=request.json['driver'],color=request.json['color'],car_type=request.json['car_type'],is_ban=request.json['is_ban'],comment=request.json['comment'])
    db.session.add(vehicle)
    db.session.commit()
    return {'id':vehicle.id}

@app.route('/plates/<plate>',methods=['GET'])
def get_vehicle(plate):
    vehicle = Vehicle.query.filter_by(plate=plate).first()
    return {
        'plate':vehicle.plate,
        'driver':vehicle.driver,
        'color':vehicle.color,
        'car_type':vehicle.car_type,
        'is_ban':vehicle.is_ban,
        'comment':vehicle.comment,
    }

@app.route('/plates/<plate>/update',methods=['PUT'])
def update_plate(plate):
    vehicle = Vehicle.query.filter_by(plate=plate).first()
    vehicle.plate = request.json['plate']
    vehicle.driver = request.json['driver']
    vehicle.color = request.json['color']
    vehicle.car_type = request.json['car_type']
    vehicle.is_ban = request.json['is_ban']
    vehicle.comment = request.json['comment']
    db.session.commit()
    return {
        'plate':vehicle.plate,
        'driver':vehicle.driver,
        'color':vehicle.color,
        'car_type':vehicle.car_type,
        'is_ban':vehicle.is_ban,
        'comment':vehicle.comment,
    }

if __name__=='__main__':
    app.run(debug=1)

     