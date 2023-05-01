# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
    return(
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    #Query of precipitation analysis
    precipitation_query = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= '2016-08-23')\
    .filter(Measurement.date <= '2017-08-23')\
    .order_by(Measurement.date).all()

    session.close()

    precipitation = []
    for date, prcp in precipitation_results:
        preceipitation_dict = {}
        preceipitation_dict["date"]= date
        preceipitation_dict["prcp"] = prcp
        precipitation.append(preceipitation_dict)
    
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    #Query of stations
    station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = []
    for station, name, latitude, longitude, elevation in station_results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        all_stations.append(stations_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    #Query of tobs
    last_row = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_row[0],'%Y-%m-%d')
    yearago_date = last_date - dt.timedelta(days=365)

    station_observation_query = session.query(Measurement.date, Measurement.tobs)\
    .filter((Measurement.date >= yearago_date), (Measurement.station =='USC00519281'))\
    .group_by(Measurement.date)\
    .order_by(Measurement.date).all()

    session.close()

    popular_tobs = []
    for date, tobs in station_observation_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        popular_tobs.append(tobs_dict)

    return jsonify(popular_tobs)


@app.route("/api/v1.0/<start>")
def start():
    #Create our session (link) from Python to the DB
    session = Session(engine)
