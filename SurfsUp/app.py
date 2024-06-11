# Import the dependencies.
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
#print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
#Session = sessionmaker(bind=engine)
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes 
# activity 10/3/10
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return(
        f"Welcome!<br/>"
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # find most recent date and date for one year prior
    most_recent_date = session.query(func.max(Measurement.date))
    one_year_prior = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # query for date and prcp data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_prior).all()

    # convert to dictionary and jsonify
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    return jsonify(precipitation_data)

# define stations route
@app.route("/api/v1.0/stations")
def stations():
    # query list of all stations
    results = session.query(Station.station).all*()
    # return jsonified list of all stations
    station_list = []
    for station, in results:
        station_list.append(station)
    
    return jsonify(station_list)

# define tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # find most active station in terms of observations
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    #narrow down data for this station
    most_active_last_date = session.query(func.max(Measurement.date)).\
        filter(Measurement.station == most_active_station)
    one_year_most_active = dt.datetime.strptime(last_date_most_active, '%Y-%m-%d') - dt.timedelta(days=365)
    #query the temp observations for this station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_most_active).all()
    #convert query results to list of dictionaries and jsonify
    tobs_data = [{'date': date, 'tobs': tobs} for date, tobs in results]

    return jsonify(tobs_data)

# define start route
# define start/end route
# define temperature statistics routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    if end:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).all()
    
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)