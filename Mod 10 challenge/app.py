# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
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
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Query for the dates and precipitation from the last year
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Query all stations
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    # Assuming 'start' is a string in 'YYYY-MM-DD' format
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    session.close()

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(results))
    return jsonify(temp_data)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    # Assuming 'start' and 'end' are strings in 'YYYY-MM-DD' format
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(results))
    return jsonify(temp_data)
if __name__ == '__main__':
    app.run(debug=True)
