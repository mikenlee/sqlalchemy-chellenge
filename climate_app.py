from sqlalchemy import create_engine
import pandas as pd

from flask import Flask, jsonify

#%%

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#%%

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#%%
#################################################
# Flask Routes
#################################################
#%%
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#%%
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = pd.read_sql('SELECT date, prcp FROM measurement', engine)
    results['prcp'] = results['prcp'].fillna('none')

    return jsonify(dict(zip(results.date, results.prcp)))

#%%
@app.route("/api/v1.0/stations")
def stations():
    
    stations = list(pd.read_sql('SELECT distinct(station) FROM measurement', engine)['station'])
    return jsonify(stations)

#%%
@app.route("/api/v1.0/tobs")
def stations():
    
    stations = list(pd.read_sql('SELECT distinct(station) FROM measurement', engine)['station'])
    return jsonify(stations)


#%%
if __name__ == '__main__':
    app.run(debug=True)

