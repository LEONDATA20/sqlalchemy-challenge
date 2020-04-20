import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement 
Station = Base.classes.station 

app = Flask(__name__)



@app.route("/api/v1.0/<start>")
def startdate(start):
    session = Session(engine) 
    dates = session.query(Measurement.date).all()

    results = session.query(Measurement.tobs)\
              .filter(Measurement.date >= start).all()
    session.close()

    TMIN = np.min(results)
    TAVG = np.mean(results)
    TMAX = np.max(results)
    result = [TMIN,TAVG,TMAX]
    for start_x in [date[0] for date in dates]:
        if start == start_x:
            return jsonify(result)
    return jsonify({"error": "start format wrong / not found."}), 404


@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(result)

    #return jsonify({"error": "start format wrong / not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)