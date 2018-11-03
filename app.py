import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Welcome!"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement).filter(Measurement.date > dt.datetime(2016, 8, 23)).\
    order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_measure = []
    for ii in results:
        measure_dict = {}
        measure_dict["date"] = ii.date
        measure_dict["temp"] = ii.tobs
        all_measure.append(measure_dict)

    return jsonify(all_measure)
    


@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    #return jsonify(all_stations)
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temps():
    
    results = session.query(Measurement.tobs).filter(Measurement.date > dt.datetime(2016, 8, 23)).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)



@app.route("/api/v1.0/<start>")
def startdate(start):
    startdate = dt.datetime.strptime(start, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= startdate).all()


    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def startenddate(start, end):
    startdate = dt.datetime.strptime(start, '%Y-%m-%d')
    enddate = dt.datetime.strptime(end, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()


    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
