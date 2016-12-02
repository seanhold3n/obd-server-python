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
cur.execute("""CREATE TABLE IF NOT EXISTS obdreadings(vehicleid TEXT, unix_timestamp BIGINT, latitude DECIMAL(11,8), longitude DECIMAL(11,8), readings JSON);""")
print('Database ready to go!')


def put(json_data):
    cur.execute("""INSERT INTO obdreadings(vehicleid, unix_timestamp, latitude, longitude, readings)
                VALUES(%s, %s, %s, %s, %s);""",
                (json_data['vehicleid'], json_data['timestamp'], json_data['latitude'], json_data['longitude'],
                 json.dumps(json_data['readings'])))
    conn.commit()


def getCur():
    return cur
