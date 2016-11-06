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
cur.execute("CREATE TABLE IF NOT EXISTS OBDREADINGS(id SERIAL, reading JSON);")
print('Database ready to go!')


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # Handle GET
    if request.method == 'GET':
        return 'Hello World!\n'

    # Handle POST
    else:
        # Get the reading
        reading = request.data

        # Store it in the DB
        cur.execute("INSERT INTO OBDREADINGS(reading) VALUES(%s);", reading)
        conn.commit()

        # Send okie-dokie response
        return Response(status=200)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
