import json
import os
import psycopg2
import urlparse

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
cur.execute("""CREATE TABLE IF NOT EXISTS obdreadings(
                      vehicleid TEXT           NOT NULL,
                      unix_timestamp BIGINT    NOT NULL,
                      latitude DECIMAL(11,8),
                      longitude DECIMAL(11,8),
                      readings JSON,
                      PRIMARY KEY (vehicleid, unix_timestamp));""")
conn.commit()
print('Database ready to go!')


def put(json_data):
    """ Stores vehicle readings data in the database.

    :param json_data:  The data as a JSON object to add to the database.  The object must contain the following keys:
        'vehicleid', a string
        'timestamp', the UNIX epoch time integer (as milliseconds)
        'latitude', a float
        'longitude', a float
        'readings', an inner JSON object
    :return: nothing.
    """
    cur.execute("""INSERT INTO obdreadings(vehicleid, unix_timestamp, latitude, longitude, readings)
                VALUES(%s, %s, %s, %s, %s);""",
                (json_data['vehicleid'], json_data['timestamp'], json_data['latitude'], json_data['longitude'],
                 json.dumps(json_data['readings'])))
    conn.commit()


def getConn():
    return conn


def getCur():
    return cur
