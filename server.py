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
cur.execute("""CREATE TABLE IF NOT EXISTS obdreadings(vin TEXT, unix_timestamp BIGINT, latitude DECIMAL(11,8), longitude DECIMAL(11,8), readings JSON);""")
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

        # Store it in the DB
        cur.execute("""INSERT INTO obdreadings(vin, unix_timestamp, latitude, longitude, readings)
                    VALUES(%s, %s, %s, %s, %s);""",
                    (json_data['vin'], json_data['timestamp'], json_data['latitude'], json_data['longitude'], json.dumps(json_data['readings'])))
        conn.commit()

        # Send okie-dokie response
        return Response(status=200)


@app.route('/view')
def view_vins():
    # Get a list of all stored vins
    cur.execute("""SELECT DISTINCT vin FROM obdreadings;""")

    # Return vin list
    return 'Available VIN records: {}'.format(str(cur.fetchall()));


@app.route('/view/<vin>')
def view_vin(vin):
    # Get the vin records from the database
    cur.execute("""SELECT * FROM obdreadings WHERE vin=%s""", (vin,))
    return str(cur.fetchall());


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
