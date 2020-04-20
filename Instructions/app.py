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


@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine) 
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    result=dict(results)
    return jsonify(result)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine) 
    stations = session.query(Measurement.station).distinct().all()
    session.close()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine) 
    station_tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-8-23").\
    filter(Measurement.station == "USC00519281").all()
    session.close()
    all_tobs=[]
    for date, tobs in station_tobs:
        tobs_dict={date:tobs}
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)


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


@app.route("/api/v1.0/<start>/<end>")
def duration(start, end):
    session = Session(engine)
    dates = session.query(Measurement.date).all()

    results = session.query(Measurement.tobs)\
              .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    TMIN = np.min(results)
    TAVG = np.mean(results)
    TMAX = np.max(results)
    result = [TMIN,TAVG,TMAX]
    #a = dt.datetime.strptime( start, "%Y-%m-%d")
    #b = dt.datetime.strptime( end, "%Y-%m-%d")
    #c=(b-a).days
    last_date = np.ravel(dates[-1])[0]

    for start in [date[0] for date in dates]:
        #dt.date(2016, 4, 8).strftime("%Y-%m-%d")
        if dt.datetime.strptime( end, "%Y-%m-%d") > dt.datetime.strptime( start, "%Y-%m-%d")\
            and dt.datetime.strptime( end, "%Y-%m-%d") < dt.datetime.strptime( last_date, "%Y-%m-%d"):
            return jsonify(result)
        else:
            return jsonify({"error": "start format wrong / not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)









    #return jsonify({"error": f"Character with real_name {start} not found."}), 404


#@app.route("/api/v1.0/<start>/<end>")
#def station(start,end):
 #   session = Session(engine) 
 #   dates = session.query(Measurement.date).all()
 #   results = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),\
 #             func.avg(Measurement.tobs)).filter().filter().all()
 #   s=start
 #   e=end
 #   for x in range (0,100):
  #      start = [date[0] for date in dates][x]
 #      if s_item == s and e_item = e:
  #          return jsonify(results)

    
 #   return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


#session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),\
#    func.avg(Measurement.tobs)).all()

    #week_ago = dt.date.today() - dt.timedelta(days=7)
    #a = dt.datetime.strptime(start, "%Y-%m-%d")
   # end = start + dt.timedelta(days=x) for x in range(0, (end-start).days))
       #end = [date[0] for date in dates]
       #start = datetime.now()
#end = start + timedelta(days=UPCOMING_DAYS)
#bdays = Birthday.query.filter(Birthday.bday <= end).filter(Birthday.bday >= start)
#    for a in start:
#        station_record = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),\
#       func.avg(Measurement.tobs)).filter(Measurement.date >= a).all()
    

   # canonicalized = real_name.replace(" ", "").lower()
    #for character in justice_league_members:
        #search_term = character["real_name"].replace(" ", "").lower()

        #if search_term == canonicalized:

 #   return jsonify(station_record)

 #   return jsonify({"error": f"Character with real_name {start} not found."}), 404




