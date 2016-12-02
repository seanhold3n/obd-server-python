import json
import os
from flask import Flask, request, Response, jsonify

# Import the database
import db

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT'])
def home():
    # Handle GET
    if request.method == 'GET':
        return 'Hello World!\n'

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

    # Return vin list
    return 'Available VIN records: {}'.format(str(db.getCur().fetchall()));


@app.route('/view/<vehicleid>')
def view_id(vehicleid):
    # Get the vehicleid records from the database
    db.getCur().execute("""SELECT * FROM obdreadings WHERE vehicleid=%s;""", (vehicleid,))
    return str(db.getCur().fetchall());


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
