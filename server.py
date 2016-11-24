import json
import os
import psycopg2
import urlparse
from flask import Flask, request, Response


app = Flask(__name__)


# Open DB connection
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
cur = conn.cursor()

# Set up obdreadings table
OBD_TABLE_NAME = 'obdreadings'
cur.execute("""CREATE TABLE IF NOT EXISTS %s(vehicleid TEXT, unix_timestamp BIGINT, latitude DECIMAL(11,8), longitude DECIMAL(11,8), readings JSON);""", (OBD_TABLE_NAME,))
print('Database ready to go!')


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
        cur.execute("""INSERT INTO %s(vehicleid, unix_timestamp, latitude, longitude, readings)
                    VALUES(%s, %s, %s, %s, %s);""",
                    (OBD_TABLE_NAME, json_data['vehicleid'], json_data['timestamp'], json_data['latitude'], json_data['longitude'],
                     json.dumps(json_data['readings'])))
        conn.commit()

        # Send okie-dokie response
        return Response(status=200)


@app.route('/view')
def view_ids():
    # Get a list of all stored vehicleids
    cur.execute("""SELECT DISTINCT vehicleid FROM %s;""", (OBD_TABLE_NAME,))

    # Return vin list
    return 'Available VIN records: {}'.format(str(cur.fetchall()));


@app.route('/view/<vehicleid>')
def view_id(vehicleid):
    # Get the vehicleid records from the database
    cur.execute("""SELECT * FROM %s WHERE vehicleid=%s""", (OBD_TABLE_NAME, vehicleid))
    return str(cur.fetchall());


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
