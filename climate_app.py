import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

 # reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Query All Records in the the Database
measurment = Base.classes.measurement
stations =Base.classes.station
# Save references to each table
session = Session(engine)
conn = engine.connect()

# Query All Records in the the Database

from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)
# Objective #1 Create home page and list all available routes
@app.route("/")
def welcome():
    return (
        f"Home Page<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )
# session = Session(engine)
# @app.route("/")
# def home():
#     return "Home Page"
# filter(measurment.date >= '2016-08-23').\
# Objective #2  Create a dictionary using date as key to list the prcp values
@app.route("/api/v1.0/precipitation")
def normal():
    session = Session(engine)
    last_year = session.query(measurment.date,measurment.prcp).\
    group_by(measurment.prcp).\
    order_by(measurment.date).all()
    session.close()
    return jsonify(last_year)
# Objective #3 Create a dictionay listing all names of stations
@app.route("/api/v1.0/stations")
def station_data():
    session = Session(engine)
    data = session.query(stations.station).all()
    session.close()
    return jsonify(data)
    
# Objective #4 Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def using():
    session = Session(engine)
    one_year = session.query(measurment.date, measurment.station,measurment.tobs).\
    filter(measurment.date >= '2016-08-18').\
    filter(measurment.station == "USC00519281").\
    order_by(measurment.date).all()
    session.close()
    return jsonify(one_year)
# Objective #5 Query to calculate the TMIN, TAVG, and TMAX and find what they equal to for the dates greater than or equal to it
# then find the calculations when putting the data within a range of dates
@app.route("/api/v1.0/<start>")
def temp(start):
    session = Session(engine)
    temperatures = session.query(func.min(measurment.tobs), func.avg(measurment.tobs), func.max(measurment.tobs)).\
    filter(measurment.date >= start).all()
    session.close()
    return jsonify(temperatures)
@app.route("/api/v1.0/<start>/<end>")
def range_temp(start,end):
    session = Session(engine)
    range_temperatures = session.query(func.min(measurment.tobs), func.avg(measurment.tobs), func.max(measurment.tobs)).\
    filter(measurment.date >= start).all()
    filter(measumrent.date <= end).all()
    session.close()
    return jsonify(range_temperatures)
if __name__ == "__main__":
    app.run(debug=True)