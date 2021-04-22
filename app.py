import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date(YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_date(YYYY-MM-DD)/end_date(YYYY-MM-DD)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dictionary of all dates and precipitation"""
    # Query all dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcps
   
    all_prcps = []

    for date, prcp in results:
        prcps_dict = {}
        prcps_dict["date"] = date
        prcps_dict["precipitation"] = prcp
        all_prcps.append(prcps_dict)

    return jsonify(all_prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    #Convert list of tuples into normal list    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    """Return a list of dictionary of all dates and temperatures"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    most_active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()

    #Find last datapoint date
    last_datapoint_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_datapoint_date = list(np.ravel(last_datapoint_date))
    last_datapoint_date = last_datapoint_date[0]

    # Convert string date into date time format
    last_datapoint_date_parsed = dt.datetime.strptime(last_datapoint_date, '%Y-%m-%d')

    #Calculate 1 year (12 months) ago
    one_year_ago_date = last_datapoint_date_parsed - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_stations[0]).\
    filter(Measurement.date >= one_year_ago_date).\
    all()

    session.close()

    # Create a dictionary from the row data and append to a list of all tobs
    all_tobs = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>") 
def temp_stats_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date only"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()

    session.close()

    # Create a dictionary from the row data and append to a list of all tobs
    temp_stats = []

    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["TMIN"] = tmin
        temp_dict["TAVG"] = tavg
        temp_dict["TMAX"] = tmax
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>") 
def temp_stats_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query the dates and temperature observations of the most active station for the last year of data.
    # print(most_active_stations)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date >= end).\
    all()
    # print(results)
    session.close()

    # Create a dictionary from the row data and append to a list of all tobs
    temp_stats = []

    for tmin, tavg, tmax in results:
        temp_dict = {}
        temp_dict["TMIN"] = tmin
        temp_dict["TAVG"] = tavg
        temp_dict["TMAX"] = tmax
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)
