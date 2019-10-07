# Import Flask
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# create app
app = Flask(__name__)

#reflect
Base = automap_base()
Base.prepare(engine, reflect = True)

#create session
session = Session(engine)

#create routes
#@app.route("/")
#def index():
 #   print("Hello server")
 #   return "Hello, world!"

#/api/v1.0/precipitation
#Convert the query results to a 
#Dictionary using date as the key and prcp as the value
@app.route("/api/v1.0/precipitation")
def precipitation():

    print("Precipitation request")

    
    date_final = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    date_max = date_final[0][0]
    max_date = datetime.datetime.strptime(date_max, "%Y-%m-%d")

    
    begin_date = max_date - datetime.timedelta(366)

    
    precip_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()
    
    #prepare the dictionary with the date as the key and the prcp value as the value
    results_dict = {}
    for result in precip_data:
        results_dict[result[0]] = result[1]

    return jsonify(results_dict)

#/api/v1.0/stations
@app.route("/contact")
def stations():

    print("Station list")

    stations_ = session.query(Station).all()

    stations_list = []
    for station in stations_:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)
#/api/v1.0/tobs

#/api/v1.0/<start> and /api/v1.0/<start>/<end>
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/tobs")
def tobs():
    print("Tobs request")

    
    date_final = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    date_max = date_final[0][0]
    max_date = datetime.datetime.strptime(date_max, "%Y-%m-%d")

    begin_date = max_date - datetime.timedelta(366)

    results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begin_date).all()

    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)
#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
