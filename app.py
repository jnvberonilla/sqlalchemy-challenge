import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """Howzit! Available API Routes for Surfs Up"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Last Year of Percipitation Data"""
    session = Session(engine)
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")

    first_date = last_date - timedelta(days=365)

    last_year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).all()
    return jsonify(last_year_data)