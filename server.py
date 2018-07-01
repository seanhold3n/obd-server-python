import json
import os
from flask import Flask, request, Response, jsonify, render_template
from datetime import datetime

# Import the database
import db
# Import API functions
import api

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT'])
def home():
    # Handle GET
    if request.method == 'GET':
        return render_template('index.html')

    # Handle POST and PUT
    else:
        # Get the reading
        json_data = json.loads(request.data)

        # Print the readings
        print str(json_data)

        # Store it in the DB
        db.put(json_data)

        # Send okie-dokie response
        return Response(status=200)


@app.route('/view')
def view_ids():
    # Get total number of database entries
    db.getCur().execute("""SELECT COUNT(*) FROM obdreadings;""")
    # Get the first item of the first tuple in the returned list
    num_rows = (db.getCur().fetchall()[0])[0]

    # Get a list of all stored vehicleids
    db.getCur().execute("""SELECT DISTINCT vehicleid FROM obdreadings;""")
    # Return id list
    ids = db.getCur().fetchall()
    # Since the above returns tuples, use a list comprehension to get the first elements
    ids = [x[0] for x in ids]

    # Get the most recent timestamp
    db.getCur().execute("""SELECT unix_timestamp from obdreadings ORDER BY unix_timestamp DESC LIMIT 1;""")
    timestamp = db.getCur().fetchone()[0] # [0] because result is a tuple - get the first element
    # Also convert timestamp to human-readable time
    int_timestamp_secs = int(timestamp) / 1000
    ts_utc = datetime.utcfromtimestamp(int_timestamp_secs).strftime('%Y-%m-%d %H:%M:%S')
    ts_local = datetime.fromtimestamp(int_timestamp_secs).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('view.html', num_rows=num_rows, ids=ids, ts_unix=timestamp, ts_utc=ts_utc, ts_local=ts_local)


@app.route('/view/<vehicleid>')
def view_id(vehicleid):
    # Get the vehicleid records from the database
    db.getCur().execute("""SELECT * FROM obdreadings WHERE vehicleid=%s;""", (vehicleid,))

    response = Response(str(db.getCur().fetchall()))
    response.mimetype = 'text/plain'
    return response;


@app.route('/api/latlong.json')
# @crossdomain(origin='*')
def get_latlong_json():
    return api.get_latlong_json()


@app.route('/api/<vehicleid>/speed.json')
# @crossdomain(origin='*')
def get_speed_json(vehicleid):
    return api.get_speed_json(vehicleid)


@app.route('/realtime')
def realtime():
    # Get 20 most recent entries
    db.getCur().execute("""SELECT * from obdreadings ORDER BY unix_timestamp DESC LIMIT 20""")

    # Publish it
    result_str = ''
    for record in db.getCur():
        result_str += '{}\n'.format(record)

    # Create and send response
    response = Response(result_str)
    response.mimetype = 'text/plain'
    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
