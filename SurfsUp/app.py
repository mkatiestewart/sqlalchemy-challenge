import datetime as dt 
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

################################################

# Create engine and setup database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to invoices 
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to Database
session = Session(engine) 

################################################

# Flask Setup

app = Flask(__name__)


# Flask Route

@app.route("/")
def welcome():
	return (
		f"Welcome to the Hawaii Climate Analysis API!</br>"
		f"Available Routes<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/temp/start/end"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	"""Return the precipitation data for the last year"""
	# Calculate the date 1 year ago from the last date in the database
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Query with the date and precipitation for the last year 
	precipitation = session.query(Measurement.date, Measurement.prcp).\
		filter(Measurement.date >= prev_year).all()

	# Dict with date as the key and prcp as the value
	precip = {date: prcp for date, prcp in precipitation}
	return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
	"""Return a list of stations."""
	results = sessions.query(Station.station).all()

	# Unravel results and convert to a list 
	stations = list(np.ravel(results))
	return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
	"""Return the temperature observations (tobs) for the previous year."""
	# Calculate the date 1 year ago from the last date in the database
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Query the primary station for all tobs from the last year
	results =  session.query(Measurement.tobs).\
	filter(Measurement.station == 'USC00519281').\
	filter(Measurement.date >= prev_year).all()

	# Unravel results and convert to a list 
	temps = list(np.ravel(results)) 
	return jsonify(temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
	"""Return TMIN, TAVG, TMAX."""


	# Select statement
	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

	if not end:
		# Calculate TMIN, TAVG, TMAX, for dates for greater than start 
		results = session.query(*sel).\
			filter(Measurement.date >= start).all()
		# Unravel results in a 1D array and convert to a list
		temps = list(np.ravel(results))
		return jsonify(temps)


# Calculate TMIN, TAVG, TMAX with start and stop
	results = session.query(*sel).\
		filter(Measurement.date >= start).\
		filter(Measurement.date <= end).all()

# Unravel results and convert to a list
	temps = list(np.ravel(results)) 
	return jsonify(temps)


if __name__ == '__main__':
	app.run()
