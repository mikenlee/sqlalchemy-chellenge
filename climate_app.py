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
def temp():
    
    #query to get temps from the most active station
    query = '''
            SELECT tobs
            FROM measurement
            WHERE station = (
                SELECT station 
                FROM (
                    SELECT COUNT(station) AS station_count , station
                    FROM measurement
                    GROUP BY station
                )
                WHERE station_count = (
                    SELECT MAX(station_count)
                    FROM (
                        SELECT count(station) AS station_count
                        FROM measurement 
                        GROUP BY station 
                ))) AND date >= "2016-08-18"
            '''
    observations = pd.read_sql(query, engine)
    return jsonify(list(observations['tobs']))

#%%
@app.route("/api/v1.0/<start>/<end>")
def calc_temp(start, end):
    
    tmax = pd.read_sql(f'SELECT max(tobs) mx FROM measurement WHERE date >= "{start}" and date <= "{end}"', engine).iloc[0][0]
    tmin = pd.read_sql(f'SELECT min(tobs) mi FROM measurement WHERE date >= "{start}" and date <= "{end}"', engine).iloc[0][0]
    tavg = pd.read_sql(f'SELECT avg(tobs) av FROM measurement WHERE date >= "{start}" and date <= "{end}"', engine).iloc[0][0]
    
    return {"max temp": tmax, "min temp": tmin, "avg temp": tavg}

#%%
@app.route("/api/v1.0/<start>")
def calc_temp(start):
    
    tmax = pd.read_sql(f'SELECT max(tobs) mx FROM measurement WHERE date >= "{start}"', engine).iloc[0][0]
    tmin = pd.read_sql(f'SELECT min(tobs) mi FROM measurement WHERE date >= "{start}"', engine).iloc[0][0]
    tavg = pd.read_sql(f'SELECT avg(tobs) av FROM measurement WHERE date >= "{start}"', engine).iloc[0][0]
    
    return {"max temp": tmax, "min temp": tmin, "avg temp": tavg}

#%%
if __name__ == '__main__':
    app.run(debug=True)

