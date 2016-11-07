# obd-server-python
Lightweight OBD server written in Python.  This is designed for use with the [android-obd-reader](https://github.com/pires/android-obd-reader) app.

## Pre-requisites
The server requires the following to read and store OBD data:
* Python 2.7
* PostgreSQL server

In addition, the server requires the installation of Flask and Psycopg2 for the web service and database connection.  These may be installed with `pip install -r requirements.txt`.

## Usage
Run server.py.  That's it!  You may now send your POST or PUT requests to the server.

You may also view all of the logs for a given VIN by going to `/view/<vin>`.

## Configuration
By default, the server will bind to port 5000, or to a port specified by a `PORT` environment variable.
The server will connect to a database through a URL given in the `DATABASE_URL` environment variable.
