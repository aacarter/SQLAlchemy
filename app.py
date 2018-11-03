from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my API!"

@app.route("/api/v1.0/precipitation")
def precipitation():
    climate = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    prec_dict = [c._asdict() for c in climate]
    return jsonify(prec_dict)

@app.route("/api/v1.0/stations")
def stations():
    list = session.query(Station.station).all()
    return jsonify(list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()
    return jsonify(tobs_query)

@app.route("/api/v1.0/<start>/<end>")
def start_temps(start, end):
    
        temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()
        x = [a._asdict() for a in temp]
        for t in x:
            if t[start] == end:
                return jsonify(t)


if __name__ == '__main__':
   app.run(debug=True)
