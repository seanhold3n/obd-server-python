import json
import os
from flask import Flask, request, Response, jsonify, render_template

# Import the database
import db

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
    # Get a list of all stored vehicleids
    db.getCur().execute("""SELECT DISTINCT vehicleid FROM obdreadings;""")

    # Return id list
    ids = db.getCur().fetchall()

    # Since the above returns tuples, use a list comprehension to get the first elements
    ids = [x[0] for x in ids]

    return render_template('view.html', ids=ids)


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
    # Get speed and timestamp data from database
    db.getCur().execute(
        """SELECT unix_timestamp,latitude,longitude from obdreadings ORDER BY unix_timestamp DESC LIMIT 100;""")  # LIMIT 500 OFFSET 100;""")

    # Start with callback handler
    callback_str = request.args.get('callback')
    if callback_str is not None:
        result_str = callback_str
        print(callback_str)
    else:
        result_str = 'callback'

    result_str += '(['

    # TODO consider jsonify here
    for record in db.getCur():
        unix_time = record[0]
        lat = record[1]
        long = record[2]
        result_str += '[{},{},{}],\n'.format(unix_time, lat, long)

    # Append end part
    result_str += ']);'

    # Create and send response
    response = Response(result_str)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


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
